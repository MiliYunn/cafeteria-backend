from __future__ import annotations

from sqlalchemy import select

from extensions import db
from models.role import Role
from services.crud_service import commit_record, delete_record, get_record, paginate_records


class RoleService:
    @staticmethod
    def list(page: int, per_page: int) -> dict:
        return paginate_records(select(Role).order_by(Role.id.desc()), page, per_page, lambda item: item.to_dict())

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
