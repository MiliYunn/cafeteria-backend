from typing import Any

from validations.common import boolean_value, required_string, validate_resource_payload

RULES = {
    "name": lambda value, field: required_string(value, field, max_length=100),
    "is_active": boolean_value,
}


def validate_genre(payload: Any, *, partial: bool = False) -> dict:
    return validate_resource_payload(payload, RULES, required={"name"}, defaults={"is_active": True}, partial=partial)
