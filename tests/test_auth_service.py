from types import SimpleNamespace
from unittest.mock import patch

import pytest

from helpers.jwt import create_refresh_token, decode_access_token, decode_refresh_token
from services.admin.auth_service import AdminAuthService
from validations.shared.exceptions import ValidationError


class ActiveAdmin:
    id = 7
    is_active = True


def test_admin_refresh_rotates_refresh_token(app):
    secret = app.config["SETTINGS"].jwt_secret
    old_refresh_token = create_refresh_token(7, "admin", secret, 7)
    database_result = SimpleNamespace(
        User=ActiveAdmin(),
        role_name="admin",
        role_is_active=True,
    )

    with (
        app.app_context(),
        patch(
            "services.shared.auth_service.db.session.execute"
        ) as execute,
        patch(
            "services.shared.auth_service.TokenService.is_revoked",
            return_value=False,
        ),
        patch("services.shared.auth_service.TokenService.revoke") as revoke,
    ):
        execute.return_value.first.return_value = database_result
        result = AdminAuthService.refresh(
            old_refresh_token,
            jwt_secret=secret,
            expires_minutes=60,
            refresh_expires_days=7,
        )

    access_payload = decode_access_token(result["access_token"], secret)
    refresh_payload = decode_refresh_token(result["refresh_token"], secret)
    old_payload = decode_refresh_token(old_refresh_token, secret)
    assert access_payload["sub"] == "7"
    assert refresh_payload["sub"] == "7"
    assert refresh_payload["jti"] != old_payload["jti"]
    revoke.assert_called_once()
    assert revoke.call_args.kwargs["jti"] == old_payload["jti"]


def test_admin_refresh_rejects_revoked_refresh_token(app):
    secret = app.config["SETTINGS"].jwt_secret
    token = create_refresh_token(7, "admin", secret, 7)

    with patch(
        "services.shared.auth_service.TokenService.is_revoked",
        return_value=True,
    ), pytest.raises(ValidationError) as caught:
        AdminAuthService.refresh(
            token,
            jwt_secret=secret,
            expires_minutes=60,
            refresh_expires_days=7,
        )

    assert caught.value.status_code == 401
    assert caught.value.message == "Refresh token has been revoked"
