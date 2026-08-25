from __future__ import annotations

from sqlalchemy import select

from extensions import db
from models.role import Role
from services.shared.crud_service import commit_record, delete_record, get_record, paginate_records
from services.shared.filter_service import apply_collection_filters


class RoleService:
    @staticmethod
    def list(page: int, per_page: int, filters: dict) -> dict:
        statement = apply_collection_filters(
            select(Role),
            filters,
            search_columns=(Role.name,),
            exact_columns={"is_active": Role.is_active},
        ).order_by(Role.id.desc())
        return paginate_records(statement, page, per_page, lambda item: item.to_dict())

    @staticmethod
    def options() -> list[dict]:
        roles = db.session.scalars(select(Role).where(Role.is_active.is_(True)).order_by(Role.name)).all()
        return [{"id": role.id, "name": role.name} for role in roles]

    @staticmethod
    def get(role_id: int) -> dict:
        return get_record(Role, role_id, "Role").to_dict()

    @staticmethod
    def create(data: dict) -> dict:
        role = Role(**data)
        db.session.add(role)
        return commit_record(role, "Role name already exists").to_dict()

    @staticmethod
    def update(role_id: int, data: dict) -> dict:
        role = get_record(Role, role_id, "Role")
        for field, value in data.items():
            setattr(role, field, value)
        return commit_record(role, "Role name already exists").to_dict()

    @staticmethod
    def delete(role_id: int) -> None:
        delete_record(get_record(Role, role_id, "Role"), "Role is being used and cannot be deleted")
