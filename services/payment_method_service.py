from __future__ import annotations

from sqlalchemy import select

from extensions import db
from models.payment_method import PaymentMethod
from services.crud_service import commit_record, delete_record, get_record, paginate_records


class PaymentMethodService:
    @staticmethod
    def list(page: int, per_page: int) -> dict:
        return paginate_records(select(PaymentMethod).order_by(PaymentMethod.id.desc()), page, per_page, lambda item: item.to_dict())

    @staticmethod
    def options() -> list[dict]:
        items = db.session.scalars(select(PaymentMethod).where(PaymentMethod.is_active.is_(True)).order_by(PaymentMethod.name)).all()
        return [{"id": item.id, "name": item.name} for item in items]

    @staticmethod
    def get(method_id: int) -> dict:
        return get_record(PaymentMethod, method_id, "Payment method").to_dict()

    @staticmethod
    def create(data: dict) -> dict:
        item = PaymentMethod(**data)
        db.session.add(item)
        return commit_record(item, "Payment method name already exists").to_dict()

    @staticmethod
    def update(method_id: int, data: dict) -> dict:
        item = get_record(PaymentMethod, method_id, "Payment method")
        for field, value in data.items():
            setattr(item, field, value)
        return commit_record(item, "Payment method name already exists").to_dict()

    @staticmethod
    def delete(method_id: int) -> None:
        delete_record(get_record(PaymentMethod, method_id, "Payment method"), "Payment method is being used and cannot be deleted")
