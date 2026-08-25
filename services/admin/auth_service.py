from datetime import datetime

from sqlalchemy import select

from extensions import db
from models.role import Role
from models.user import User
from services.shared.auth_service import AuthService
from services.shared.token_service import TokenService
from validations.shared.exceptions import ValidationError


class AdminAuthService:
    @staticmethod
    def login(
        email: str,
        password: str,
        *,
        jwt_secret: str,
        expires_minutes: int,
        refresh_expires_days: int,
    ) -> dict:
        return AuthService.login(
            email,
            password,
            jwt_secret=jwt_secret,
            expires_minutes=expires_minutes,
            refresh_expires_days=refresh_expires_days,
            allowed_roles={"admin"},
            email_only=True,
        )

    @staticmethod
    def logout(*, jti: str, user_id: int, expires_at: datetime) -> None:
        TokenService.revoke(jti=jti, user_id=user_id, expires_at=expires_at)

    @staticmethod
    def refresh(
        refresh_token: str,
        *,
        jwt_secret: str,
        expires_minutes: int,
        refresh_expires_days: int,
    ) -> dict:
        return AuthService.refresh(
            refresh_token,
            jwt_secret=jwt_secret,
            expires_minutes=expires_minutes,
            refresh_expires_days=refresh_expires_days,
            allowed_roles={"admin"},
        )

    @staticmethod
    def profile(user_id: int) -> dict:
        result = db.session.execute(
            select(User, Role.name.label("role_name"))
            .join(Role, User.role_id == Role.id)
            .where(User.id == user_id)
        ).first()
        if result is None:
            raise ValidationError("Authenticated user was not found", status_code=404)
        profile = result.User.to_dict(exclude={"password"})
        profile["role"] = result.role_name
        return profile
