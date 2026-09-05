"""Request validation for settings controlled by a shop."""

from typing import Any

from validations.shared.fields import clock_time, validate_resource_payload


RULES = {
    "open_at": clock_time,
    "close_at": clock_time,
}


def validate_shop_settings(payload: Any) -> dict:
    return validate_resource_payload(payload, RULES, partial=True)
