from __future__ import annotations

from sqlalchemy import select

from extensions import db
from models.payment_account import PaymentAccount
from models.payment_method import PaymentMethod
from models.shop import Shop
from services.crud_service import commit_record, delete_record, get_record, paginate_records
from validations.exceptions import ValidationError


class PaymentAccountService:
    @staticmethod
    def _shop(shop_id: int) -> None:
        get_record(Shop, shop_id, "Shop")

    @staticmethod
    def _account(shop_id: int, account_id: int) -> PaymentAccount:
        account = get_record(PaymentAccount, account_id, "Payment account")
        if account.shop_id != shop_id:
            raise ValidationError("Payment account not found", status_code=404)
        return account

    @staticmethod
    def _method(method_id: int) -> None:
        get_record(PaymentMethod, method_id, "Payment method")

    @staticmethod
    def list(shop_id: int, page: int, per_page: int) -> dict:
        PaymentAccountService._shop(shop_id)
        statement = select(PaymentAccount).where(PaymentAccount.shop_id == shop_id).order_by(PaymentAccount.id.desc())
        return paginate_records(statement, page, per_page, lambda item: item.to_dict())

    @staticmethod
    def get(shop_id: int, account_id: int) -> dict:
        return PaymentAccountService._account(shop_id, account_id).to_dict()

    @staticmethod
    def create(shop_id: int, data: dict) -> dict:
        PaymentAccountService._shop(shop_id)
        PaymentAccountService._method(data["payment_method_id"])
        account = PaymentAccount(shop_id=shop_id, **data)
        db.session.add(account)
        return commit_record(account, "Payment account could not be created").to_dict()

    @staticmethod
    def update(shop_id: int, account_id: int, data: dict) -> dict:
        account = PaymentAccountService._account(shop_id, account_id)
        if "payment_method_id" in data:
            PaymentAccountService._method(data["payment_method_id"])
        for field, value in data.items():
            setattr(account, field, value)
        return commit_record(account, "Payment account could not be updated").to_dict()

    @staticmethod
    def delete(shop_id: int, account_id: int) -> None:
        delete_record(PaymentAccountService._account(shop_id, account_id), "Payment account is being used and cannot be deleted")
