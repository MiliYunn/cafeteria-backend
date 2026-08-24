"""Category payload validation."""

from typing import Any

from validations.common import boolean_value, optional_string, required_string, validate_resource_payload

RULES = {
    "name": lambda value, field: required_string(value, field, max_length=100),
    "description": lambda value, field: optional_string(value, field, max_length=5000),
    "is_active": boolean_value,
}


def validate_category(payload: Any, *, partial: bool = False) -> dict[str, Any]:
    return validate_resource_payload(payload, RULES, required={"name"}, defaults={"is_active": True}, partial=partial)


def validate_category_create(payload: Any) -> dict[str, Any]:
    return validate_category(payload)
