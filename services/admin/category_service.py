from __future__ import annotations

from sqlalchemy import select

from extensions import db
from models.category import Category
from services.shared.crud_service import commit_record, delete_record, get_record, paginate_records
from services.shared.filter_service import apply_collection_filters


class CategoryService:
    @staticmethod
    def list(page: int, per_page: int, filters: dict) -> dict:
        statement = apply_collection_filters(
            select(Category),
            filters,
            search_columns=(Category.name, Category.description),
            exact_columns={"is_active": Category.is_active},
        ).order_by(Category.id.desc())
        return paginate_records(statement, page, per_page, lambda item: item.to_dict())

    @staticmethod
    def options() -> list[dict]:
        items = db.session.scalars(select(Category).where(Category.is_active.is_(True)).order_by(Category.name)).all()
        return [{"id": item.id, "name": item.name} for item in items]

    @staticmethod
    def get(category_id: int) -> dict:
        return get_record(Category, category_id, "Category").to_dict()

    @staticmethod
    def create(data: dict) -> dict:
        item = Category(**data)
        db.session.add(item)
        return commit_record(item, "Category name already exists").to_dict()

    @staticmethod
    def update(category_id: int, data: dict) -> dict:
        item = get_record(Category, category_id, "Category")
        for field, value in data.items():
            setattr(item, field, value)
        return commit_record(item, "Category name already exists").to_dict()

    @staticmethod
    def delete(category_id: int) -> None:
        delete_record(get_record(Category, category_id, "Category"), "Category is being used and cannot be deleted")
