"""Admin authentication payload validation."""

from typing import Any

from validations.shared.auth import validate_email_login
from validations.shared.fields import required_string, validate_resource_payload


def validate_admin_login(payload: Any) -> dict[str, str]:
    return validate_email_login(payload)


def validate_refresh_token(payload: Any) -> dict[str, str]:
    return validate_resource_payload(
        payload,
        {
            "refresh_token": lambda value, field: required_string(
                value,
                field,
                max_length=4096,
            ),
        },
        required={"refresh_token"},
    )
