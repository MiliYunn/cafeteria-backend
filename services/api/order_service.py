"""Customer ordering workflows with server-calculated totals."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import select

from extensions import db
from models.menu import Menu
from models.order import Order
from models.order_log import OrderLog
from models.order_menu import OrderMenu
from models.payment_account import PaymentAccount
from models.payment_method import PaymentMethod
from models.shop import Shop
from models.user import User
from services.shared.crud_service import paginate_records
from services.shared.order_fee_service import OrderFeeService
from validations.shared.exceptions import ValidationError


class OrderService:
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
        shop = db.session.get(Shop, order.shop_id)
        data["shop"] = {"id": shop.id, "name": shop.name} if shop else None
        data["items"] = [
            {
                **item.to_dict(),
                "menu_name": menu_name,
            }
            for item, menu_name in items
        ]
        if payment:
            data["payment_account"] = {
                **payment.PaymentAccount.to_dict(),
                "payment_method": payment.PaymentMethod.to_dict(),
            }
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
    def create(user_id: int, data: dict) -> dict:
        user = db.session.get(User, user_id)
        shop = db.session.get(Shop, data["shop_id"])
        if user is None or not user.is_active:
            raise ValidationError("User not found", status_code=404)
        if shop is None or not shop.is_active:
            raise ValidationError("Shop not found", status_code=404)

        payment = db.session.execute(
            select(PaymentAccount, PaymentMethod)
            .join(PaymentMethod, PaymentMethod.id == PaymentAccount.payment_method_id)
            .where(
                PaymentAccount.id == data["payment_account_id"],
                PaymentAccount.shop_id == shop.id,
                PaymentAccount.is_active.is_(True),
                PaymentMethod.is_active.is_(True),
            )
        ).first()
        if payment is None:
            raise ValidationError(
                errors={"payment_account_id": "Payment account is not available"}
            )
        if payment.PaymentMethod.type.lower() == "cash" and data["fulfillment"] != "pickup":
            raise ValidationError(
                errors={"fulfillment": "Cash orders are available for pickup only"}
            )

        requested = {item["menu_id"]: item["quantity"] for item in data["items"]}
        menus = db.session.scalars(
            select(Menu).where(
                Menu.id.in_(requested),
                Menu.shop_id == shop.id,
                Menu.is_available.is_(True),
            )
        ).all()
        if len(menus) != len(requested):
            raise ValidationError(errors={"items": "One or more menu items are unavailable"})

        subtotal = sum(
            (menu.cost * requested[menu.id] for menu in menus), Decimal("0.00")
        ).quantize(Decimal("0.01"))
        fees = OrderFeeService.calculate(subtotal, data["fulfillment"])
        order = Order(
            shop_id=shop.id,
            user_id=user.id,
            user_email=user.email,
            order_code=f"APC-{datetime.now(UTC):%Y%m%d}-{uuid4().hex[:8].upper()}",
            status="pending",
            subtotal_amount=fees.subtotal_amount,
            total_amount=fees.total_amount,
            remark=data.get("remark"),
            payment_account_id=payment.PaymentAccount.id,
            tax_fee=fees.tax_fee,
            service_fee=fees.service_fee,
            is_pickup=data["fulfillment"] == "pickup",
            delivery_location=(
                None if data["fulfillment"] == "pickup" else data["delivery_location"]
            ),
        )
        db.session.add(order)
        db.session.flush()
        db.session.add_all(
            OrderMenu(
                order_id=order.id,
                menu_id=menu.id,
                quantity=requested[menu.id],
                amount=(menu.cost * requested[menu.id]).quantize(Decimal("0.01")),
            )
            for menu in menus
        )
        db.session.add(OrderLog(order_id=order.id, status="pending", user_id=user.id))
        db.session.commit()
        db.session.refresh(order)
        return OrderService._serialize(order, include_history=True)

    @staticmethod
    def list(user_id: int, page: int, per_page: int) -> dict:
        statement = (
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.order_at.desc(), Order.id.desc())
        )
        return paginate_records(statement, page, per_page, OrderService._serialize)

    @staticmethod
    def get(user_id: int, order_id: int) -> dict:
        order = db.session.get(Order, order_id)
        if order is None or order.user_id != user_id:
            raise ValidationError("Order not found", status_code=404)
        return OrderService._serialize(order, include_history=True)
