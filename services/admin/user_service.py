from __future__ import annotations

from sqlalchemy import select

from extensions import db
from helpers.hash import hash_password
from models.role import Role
from models.user import User
from services.shared.crud_service import commit_record, delete_record, get_record, paginate_records
from services.shared.filter_service import apply_collection_filters
from validations.shared.exceptions import ValidationError


def _serialize(user: User) -> dict:
    return user.to_dict(exclude={"password"})


class UserService:
    @staticmethod
    def _ensure_role(role_id: int) -> None:
        get_record(Role, role_id, "Role")

    @staticmethod
    def list(page: int, per_page: int, filters: dict) -> dict:
        statement = apply_collection_filters(
            select(User),
            filters,
            search_columns=(User.username, User.email, User.fullname),
            exact_columns={
                "is_active": User.is_active,
                "role_id": User.role_id,
                "department_id": User.department_id,
                "type": User.type,
            },
        ).order_by(User.id.desc())
        return paginate_records(statement, page, per_page, _serialize)

    @staticmethod
    def get(user_id: int) -> dict:
        return _serialize(get_record(User, user_id, "User"))

    @staticmethod
    def create(data: dict) -> dict:
        UserService._ensure_role(data["role_id"])
        data["password"] = hash_password(data["password"])
        user = User(**data)
        db.session.add(user)
        return _serialize(commit_record(user, "Username or email already exists"))

    @staticmethod
    def update(user_id: int, data: dict) -> dict:
        user = get_record(User, user_id, "User")
        if "role_id" in data:
            UserService._ensure_role(data["role_id"])
        if "password" in data:
            data["password"] = hash_password(data["password"])
        for field, value in data.items():
            setattr(user, field, value)
        return _serialize(commit_record(user, "Username or email already exists"))

    @staticmethod
    def delete(user_id: int, current_user_id: int) -> None:
        if user_id == current_user_id:
            raise ValidationError("You cannot delete your own account", status_code=409)
        delete_record(get_record(User, user_id, "User"), "User has related records and cannot be deleted")
