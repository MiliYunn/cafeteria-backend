from datetime import UTC, datetime

from flask import current_app, g, request

from helpers.response import success_response
from services.api.auth_service import ApiAuthService
from validations.api.auth import validate_api_login


def student_login():
    data = validate_api_login(request.get_json(silent=True))
    settings = current_app.config["SETTINGS"]
    result = ApiAuthService.login(
        data["email"],
        data["password"],
        jwt_secret=settings.jwt_secret,
        expires_minutes=settings.jwt_expires_minutes,
    )
    return success_response(result, "Login successful")


def student_logout():
    payload = g.auth
    ApiAuthService.logout(
        jti=payload["jti"],
        user_id=int(payload["sub"]),
        expires_at=datetime.fromtimestamp(payload["exp"], tz=UTC),
    )
    return success_response(message="Logout successful")
