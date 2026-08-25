from typing import Any

from validations.shared.fields import boolean_value, optional_string, required_string, valid_url, validate_resource_payload

RULES = {
    "name": lambda value, field: required_string(value, field, max_length=100),
    "description": lambda value, field: optional_string(value, field, max_length=5000),
    "logo": valid_url,
    "domain_url": valid_url,
    "is_active": boolean_value,
    "type": lambda value, field: required_string(value, field, max_length=50),
}


def validate_payment_method(payload: Any, *, partial: bool = False) -> dict:
    return validate_resource_payload(payload, RULES, required={"name", "type"}, defaults={"is_active": True}, partial=partial)
