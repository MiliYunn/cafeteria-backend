from typing import Any

from validations.shared.fields import (
    boolean_value,
    iso_datetime,
    optional_string,
    required_string,
    valid_email,
    valid_url,
    validate_resource_payload,
)

RULES = {
    "name": lambda value, field: required_string(value, field, max_length=150),
    "description": lambda value, field: optional_string(value, field, max_length=5000),
    "logo_url": valid_url,
    "location": lambda value, field: required_string(value, field, max_length=255),
    "is_active": boolean_value,
    "email": valid_email,
    "password": lambda value, field: required_string(value, field, min_length=8, max_length=128),
    "open_at": iso_datetime,
    "close_at": iso_datetime,
}


def validate_shop(payload: Any, *, partial: bool = False) -> dict:
    return validate_resource_payload(
        payload,
        RULES,
        required={"name", "location", "email", "password"},
        defaults={"description": None, "logo_url": None, "is_active": True, "open_at": None, "close_at": None},
        partial=partial,
    )
