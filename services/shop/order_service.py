"""Shop-scoped customer order management."""

from sqlalchemy import select

from extensions import db
from models.menu import Menu
from models.order import Order
from models.order_log import OrderLog
from models.order_menu import OrderMenu
from models.payment_account import PaymentAccount
from models.payment_method import PaymentMethod
from models.user import User
from services.shared.crud_service import paginate_records
from services.shared.filter_service import apply_collection_filters
from validations.shared.exceptions import ValidationError


class ShopOrderService:
    TRANSITIONS = {
        "pending": {"confirmed", "cancelled"},
        "confirmed": {"preparing", "cancelled"},
        "preparing": {"ready", "cancelled"},
        "ready": {"completed"},
        "completed": set(),
        "cancelled": set(),
    }

    @staticmethod
    def _order(shop_id: int, order_id: int) -> Order:
        order = db.session.get(Order, order_id)
        if order is None or order.shop_id != shop_id:
            raise ValidationError("Order not found", status_code=404)
        return order

    @staticmethod
    def _serialize(order: Order, *, include_history: bool = False) -> dict:
        data = order.to_dict()
        items = db.session.execute(
            select(OrderMenu, Menu.name)
            .join(Menu, Menu.id == OrderMenu.menu_id)
            .where(OrderMenu.order_id == order.id)
            .order_by(OrderMenu.id)
        ).all()
        payment = db.session.execute(
            select(PaymentAccount, PaymentMethod)
            .join(PaymentMethod, PaymentMethod.id == PaymentAccount.payment_method_id)
            .where(PaymentAccount.id == order.payment_account_id)
        ).first()
        customer = db.session.get(User, order.user_id)
        data["items"] = [
            {**item.to_dict(), "menu_name": menu_name}
            for item, menu_name in items
        ]
        data["customer"] = (
            {
                "id": customer.id,
                "fullname": customer.fullname,
                "email": customer.email,
            }
            if customer
            else {"id": order.user_id, "fullname": order.user_email, "email": order.user_email}
        )
        data["payment_account"] = (
            {
                **payment.PaymentAccount.to_dict(),
                "payment_method": payment.PaymentMethod.to_dict(),
            }
            if payment
            else None
        )
        if include_history:
            history = db.session.scalars(
                select(OrderLog)
                .where(OrderLog.order_id == order.id)
                .order_by(OrderLog.created_at, OrderLog.id)
            ).all()
            data["status_history"] = [
                log.to_dict(exclude={"user_id", "updated_at"}) for log in history
            ]
        return data

    @staticmethod
    def list(shop_id: int, page: int, per_page: int, filters: dict) -> dict:
        fulfillment = filters.pop("fulfillment", None)
        statement = apply_collection_filters(
            select(Order).where(Order.shop_id == shop_id),
            filters,
            search_columns=(Order.order_code, Order.user_email),
            exact_columns={"status": Order.status},
        )
        if fulfillment:
            statement = statement.where(Order.is_pickup.is_(fulfillment == "pickup"))
        statement = statement.order_by(Order.order_at.desc(), Order.id.desc())
        return paginate_records(statement, page, per_page, ShopOrderService._serialize)

    @staticmethod
    def get(shop_id: int, order_id: int) -> dict:
        return ShopOrderService._serialize(
            ShopOrderService._order(shop_id, order_id), include_history=True
        )

    @staticmethod
    def update_status(shop_id: int, order_id: int, status: str) -> dict:
        order = ShopOrderService._order(shop_id, order_id)
        allowed = ShopOrderService.TRANSITIONS.get(order.status, set())
        if status not in allowed:
            choices = ", ".join(sorted(allowed)) or "none"
            raise ValidationError(
                errors={"status": f"Cannot change {order.status} order to {status}. Allowed: {choices}"}
            )
        order.status = status
        db.session.add(OrderLog(order_id=order.id, status=status, user_id=None))
        db.session.commit()
        db.session.refresh(order)
        return ShopOrderService._serialize(order, include_history=True)
