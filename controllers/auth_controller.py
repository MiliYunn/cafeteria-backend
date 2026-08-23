from datetime import UTC, datetime

from flask import current_app, g, request

from helpers.response import success_response
from services.auth_service import AuthService
from services.token_service import TokenService
from validations.auth import validate_login


def _login(allowed_roles: set[str]):
    data = validate_login(request.get_json(silent=True))
    settings = current_app.config["SETTINGS"]
    result = AuthService.login(
        data["login"],
        data["password"],
        jwt_secret=settings.jwt_secret,
        expires_minutes=settings.jwt_expires_minutes,
        allowed_roles=allowed_roles,
    )
    return success_response(result, "Login successful")


def admin_login():
    return _login({"admin"})


def student_login():
    return _login({"student"})


def logout():
    payload = g.auth
    TokenService.revoke(
        jti=payload["jti"],
        user_id=int(payload["sub"]),
        expires_at=datetime.fromtimestamp(payload["exp"], tz=UTC),
    )
    return success_response(message="Logout successful")
