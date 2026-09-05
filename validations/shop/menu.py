"""Request validation for shop-owned menu items."""

from typing import Any

from validations.shared.fields import (
    boolean_value,
    non_negative_decimal,
    optional_string,
    positive_integer_list,
    required_string,
    valid_url,
    validate_resource_payload,
)


def _genre_ids(value: Any, field: str) -> list[int]:
    values = positive_integer_list(value, field)
    if not values:
        raise ValueError(f"{field} must contain at least one genre")
    return values


RULES = {
    "genre_ids": _genre_ids,
    "name": lambda value, field: required_string(value, field, max_length=150),
    "cost": non_negative_decimal,
    "is_available": boolean_value,
    "image": valid_url,
    "description": lambda value, field: optional_string(value, field, max_length=2000),
}


def validate_menu(payload: Any, *, partial: bool = False) -> dict:
    return validate_resource_payload(
        payload,
        RULES,
        required={"genre_ids", "name", "cost"},
        defaults={"is_available": True, "image": None, "description": None},
        partial=partial,
    )
