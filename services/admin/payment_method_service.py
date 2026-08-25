from __future__ import annotations

from sqlalchemy import select

from extensions import db
from models.payment_method import PaymentMethod
from services.shared.crud_service import commit_record, delete_record, get_record, paginate_records
from services.shared.filter_service import apply_collection_filters


class PaymentMethodService:
    @staticmethod
    def list(page: int, per_page: int, filters: dict) -> dict:
        statement = apply_collection_filters(
            select(PaymentMethod),
            filters,
            search_columns=(PaymentMethod.name, PaymentMethod.description),
            exact_columns={
                "is_active": PaymentMethod.is_active,
                "type": PaymentMethod.type,
            },
        ).order_by(PaymentMethod.id.desc())
        return paginate_records(statement, page, per_page, lambda item: item.to_dict())

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
