"""Authentication and refresh-token workflows."""

from datetime import UTC, datetime

import jwt
from sqlalchemy import or_, select

from extensions import db
from helpers.hash import verify_password
from helpers.jwt import create_access_token, create_refresh_token, decode_refresh_token
from models.role import Role
from models.user import User
from services.shared.token_service import TokenService
from validations.shared.exceptions import ValidationError


def _create_token_pair(
    user_id: int,
    role: str,
    *,
    jwt_secret: str,
    expires_minutes: int,
    refresh_expires_days: int,
) -> dict:
    return {
        "access_token": create_access_token(
            user_id,
            role,
            jwt_secret,
            expires_minutes,
        ),
        "refresh_token": create_refresh_token(
            user_id,
            role,
            jwt_secret,
            refresh_expires_days,
        ),
        "token_type": "Bearer",
        "expires_in": expires_minutes * 60,
        "refresh_expires_in": refresh_expires_days * 24 * 60 * 60,
    }


class AuthService:
    @staticmethod
    def login(
        login: str,
        password: str,
        *,
        jwt_secret: str,
        expires_minutes: int,
        refresh_expires_days: int | None = None,
        allowed_roles: set[str],
        email_only: bool = False,
    ) -> dict:
        identity_filter = User.email == login.lower()
        if not email_only:
            identity_filter = or_(User.username == login, identity_filter)
        statement = (
            select(
                User,
                Role.name.label("role_name"),
                Role.is_active.label("role_is_active"),
            )
            .join(Role, User.role_id == Role.id)
            .where(identity_filter)
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
        tokens = {
            "access_token": create_access_token(
                result.User.id,
                result.role_name,
                jwt_secret,
                expires_minutes,
            ),
            "token_type": "Bearer",
            "expires_in": expires_minutes * 60,
            "user": result.User.to_dict(exclude={"password"}),
            "role": result.role_name,
        }
        if refresh_expires_days is not None:
            tokens.update(
                {
                    "refresh_token": create_refresh_token(
                        result.User.id,
                        result.role_name,
                        jwt_secret,
                        refresh_expires_days,
                    ),
                    "refresh_expires_in": refresh_expires_days * 24 * 60 * 60,
                }
            )
        return tokens

    @staticmethod
    def refresh(
        refresh_token: str,
        *,
        jwt_secret: str,
        expires_minutes: int,
        refresh_expires_days: int,
        allowed_roles: set[str],
    ) -> dict:
        try:
            payload = decode_refresh_token(refresh_token, jwt_secret)
            user_id = int(payload["sub"])
        except jwt.ExpiredSignatureError as exc:
            raise ValidationError("Refresh token has expired", status_code=401) from exc
        except (jwt.InvalidTokenError, TypeError, ValueError) as exc:
            raise ValidationError("Invalid refresh token", status_code=401) from exc

        if TokenService.is_revoked(payload["jti"]):
            raise ValidationError("Refresh token has been revoked", status_code=401)

        result = db.session.execute(
            select(
                User,
                Role.name.label("role_name"),
                Role.is_active.label("role_is_active"),
            )
            .join(Role, User.role_id == Role.id)
            .where(User.id == user_id)
        ).first()
        if (
            not result
            or not result.User.is_active
            or not result.role_is_active
            or result.role_name not in allowed_roles
            or payload.get("role") != result.role_name
        ):
            raise ValidationError("Refresh token is not authorized", status_code=401)

        TokenService.revoke(
            jti=payload["jti"],
            user_id=user_id,
            expires_at=datetime.fromtimestamp(payload["exp"], tz=UTC),
        )
        return _create_token_pair(
            user_id,
            result.role_name,
            jwt_secret=jwt_secret,
            expires_minutes=expires_minutes,
            refresh_expires_days=refresh_expires_days,
        )
