"""Authentication workflow."""

from sqlalchemy import or_, select

from extensions import db
from helpers.hash import verify_password
from helpers.jwt import create_access_token
from models.role import Role
from models.user import User
from validations.exceptions import ValidationError


class AuthService:
    @staticmethod
    def login(
        login: str,
        password: str,
        *,
        jwt_secret: str,
        expires_minutes: int,
        allowed_roles: set[str],
    ) -> dict:
        statement = (
            select(
                User,
                Role.name.label("role_name"),
                Role.is_active.label("role_is_active"),
            )
            .join(Role, User.role_id == Role.id)
            .where(or_(User.username == login, User.email == login.lower()))
        )
        result = db.session.execute(statement).first()
        if (
            not result
            or not result.User.is_active
            or not result.role_is_active
            or result.role_name not in allowed_roles
            or not verify_password(password, result.User.password)
        ):
            raise ValidationError("Invalid credentials", status_code=401)
        token = create_access_token(result.User.id, result.role_name, jwt_secret, expires_minutes)
        return {
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": expires_minutes * 60,
            "user": result.User.to_dict(exclude={"password"}),
            "role": result.role_name,
        }
