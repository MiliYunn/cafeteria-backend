"""Staff and student profile workflows."""

from extensions import db
from helpers.hash import hash_password
from models.user import User
from services.shared.crud_service import commit_record
from validations.shared.exceptions import ValidationError


class ProfileService:
    @staticmethod
    def get(user_id: int) -> dict:
        user = db.session.get(User, user_id)
        if user is None or not user.is_active:
            raise ValidationError("User not found", status_code=404)
        return user.to_dict(exclude={"password"})

    @staticmethod
    def update(user_id: int, data: dict) -> dict:
        user = db.session.get(User, user_id)
        if user is None or not user.is_active:
            raise ValidationError("User not found", status_code=404)
        if "fullname" in data:
            user.fullname = data["fullname"]
        if "password" in data:
            user.password = hash_password(data["password"])
        return commit_record(user, "Profile could not be updated").to_dict(
            exclude={"password"}
        )
