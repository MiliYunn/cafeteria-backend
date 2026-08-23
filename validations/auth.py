"""Authentication payload validation."""

from typing import Any

from validations.common import required_string
from validations.exceptions import ValidationError


def validate_login(payload: Any) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise ValidationError(errors={"body": "A JSON object is required"})
    errors: dict[str, str] = {}
    result: dict[str, str] = {}
    for field, maximum in (("login", 255), ("password", 128)):
        try:
            result[field] = required_string(payload.get(field), field, max_length=maximum)
        except ValueError as exc:
            errors[field] = str(exc)
    if errors:
        raise ValidationError(errors=errors)
    return result

