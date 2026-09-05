"""Validation for staff and student profile updates."""

from typing import Any

from validations.shared.fields import required_string, validate_resource_payload


RULES = {
    "fullname": lambda value, field: required_string(value, field, max_length=255),
    "password": lambda value, field: required_string(
        value, field, min_length=8, max_length=15
    ),
}


def validate_profile_update(payload: Any) -> dict:
    return validate_resource_payload(payload, RULES, partial=True)
