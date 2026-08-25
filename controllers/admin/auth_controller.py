from datetime import UTC, datetime

from flask import current_app, g, request

from helpers.response import success_response
from services.admin.auth_service import AdminAuthService
from validations.admin.auth import validate_admin_login, validate_refresh_token


def admin_login():
    data = validate_admin_login(request.get_json(silent=True))
    settings = current_app.config["SETTINGS"]
    result = AdminAuthService.login(
        data["email"],
        data["password"],
        jwt_secret=settings.jwt_secret,
        expires_minutes=settings.jwt_expires_minutes,
        refresh_expires_days=settings.jwt_refresh_expires_days,
    )
    return success_response(result, "Login successful")


def admin_logout():
    payload = g.auth
    AdminAuthService.logout(
        jti=payload["jti"],
        user_id=int(payload["sub"]),
        expires_at=datetime.fromtimestamp(payload["exp"], tz=UTC),
    )
    return success_response(message="Logout successful")


def admin_profile():
    profile = AdminAuthService.profile(int(g.auth["sub"]))
    return success_response(profile, "Profile retrieved")


def admin_revoke_token():
    payload = g.auth
    AdminAuthService.logout(
        jti=payload["jti"],
        user_id=int(payload["sub"]),
        expires_at=datetime.fromtimestamp(payload["exp"], tz=UTC),
    )
    return success_response(message="Token revoked successfully")


def admin_refresh_token():
    data = validate_refresh_token(request.get_json(silent=True))
    settings = current_app.config["SETTINGS"]
    result = AdminAuthService.refresh(
        data["refresh_token"],
        jwt_secret=settings.jwt_secret,
        expires_minutes=settings.jwt_expires_minutes,
        refresh_expires_days=settings.jwt_refresh_expires_days,
    )
    return success_response(result, "Token refreshed successfully")
