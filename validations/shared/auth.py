"""Shared email-and-password authentication payload validation."""

from typing import Any

from validations.shared.fields import required_string, valid_email, validate_resource_payload


def validate_email_login(payload: Any) -> dict[str, str]:
    return validate_resource_payload(
        payload,
        {
            "email": valid_email,
            "password": lambda value, field: required_string(value, field, max_length=15),
        },
        required={"email", "password"},
    )
