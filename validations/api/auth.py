"""Student API authentication payload validation."""

from typing import Any

from validations.shared.auth import validate_email_login


def validate_api_login(payload: Any) -> dict[str, str]:
    return validate_email_login(payload)
