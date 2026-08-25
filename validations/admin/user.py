from typing import Any

from validations.shared.fields import (
    boolean_value,
    nullable_positive_integer,
    positive_integer,
    required_string,
    valid_email,
    validate_resource_payload,
)

RULES = {
    "username": lambda value, field: required_string(value, field, min_length=3, max_length=100),
    "email": valid_email,
    "fullname": lambda value, field: required_string(value, field, max_length=255),
    "role_id": positive_integer,
    "department_id": nullable_positive_integer,
    "password": lambda value, field: required_string(value, field, min_length=8, max_length=128),
    "is_active": boolean_value,
    "type": lambda value, field: required_string(value, field, max_length=50),
}


def validate_user(payload: Any, *, partial: bool = False) -> dict:
    return validate_resource_payload(
        payload,
        RULES,
        required={"username", "email", "fullname", "role_id", "password", "type"},
        defaults={"department_id": None, "is_active": True},
        partial=partial,
    )
