"""Category payload validation."""

from typing import Any

from validations.common import required_string
from validations.exceptions import ValidationError


def validate_category_create(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValidationError(errors={"body": "A JSON object is required"})
    errors: dict[str, str] = {}
    result: dict[str, Any] = {}
    try:
        result["name"] = required_string(payload.get("name"), "name", max_length=100)
    except ValueError as exc:
        errors["name"] = str(exc)
    description = payload.get("description")
    if description is not None:
        try:
            result["description"] = required_string(description, "description", max_length=5000)
        except ValueError as exc:
            errors["description"] = str(exc)
    result["is_active"] = payload.get("is_active", True)
    if not isinstance(result["is_active"], bool):
        errors["is_active"] = "is_active must be a boolean"
    if errors:
        raise ValidationError(errors=errors)
    return result

