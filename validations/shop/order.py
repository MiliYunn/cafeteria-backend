"""Request validation for shop order status changes."""

from typing import Any

from validations.shared.fields import one_of, validate_resource_payload
from validations.shop.filters import ORDER_STATUSES


def validate_order_status(payload: Any) -> dict:
    return validate_resource_payload(
        payload,
        {"status": lambda value, field: one_of(value, field, ORDER_STATUSES)},
        required={"status"},
    )
