from datetime import datetime

from services.shared.auth_service import AuthService
from services.shared.token_service import TokenService


class ApiAuthService:
    @staticmethod
    def login(email: str, password: str, *, jwt_secret: str, expires_minutes: int) -> dict:
        return AuthService.login(
            email,
            password,
            jwt_secret=jwt_secret,
            expires_minutes=expires_minutes,
            allowed_roles={"student"},
            email_only=True,
        )

    @staticmethod
    def logout(*, jti: str, user_id: int, expires_at: datetime) -> None:
        TokenService.revoke(jti=jti, user_id=user_id, expires_at=expires_at)
