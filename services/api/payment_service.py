"""Customer-facing payment choices for a shop."""

from sqlalchemy import select

from extensions import db
from models.payment_account import PaymentAccount
from models.payment_method import PaymentMethod
from models.shop import Shop
from validations.shared.exceptions import ValidationError


class PaymentService:
    @staticmethod
    def list_for_shop(shop_id: int) -> list[dict]:
        shop = db.session.get(Shop, shop_id)
        if shop is None or not shop.is_active:
            raise ValidationError("Shop not found", status_code=404)
        rows = db.session.execute(
            select(PaymentAccount, PaymentMethod)
            .join(PaymentMethod, PaymentMethod.id == PaymentAccount.payment_method_id)
            .where(
                PaymentAccount.shop_id == shop_id,
                PaymentAccount.is_active.is_(True),
                PaymentMethod.is_active.is_(True),
            )
            .order_by(PaymentMethod.type, PaymentMethod.name)
        ).all()
        return [
            {
                **account.to_dict(),
                "payment_method": method.to_dict(),
            }
            for account, method in rows
        ]
