"""Request validation for customer order creation."""

from typing import Any

from validations.shared.exceptions import ValidationError
from validations.shared.fields import (
    one_of,
    optional_string,
    positive_integer,
    require_json_object,
)


def validate_order(payload: Any) -> dict:
    body = require_json_object(payload)
    allowed = {
        "shop_id",
        "payment_account_id",
        "fulfillment",
        "delivery_location",
        "remark",
        "items",
    }
    errors = {field: f"{field} is not allowed" for field in set(body) - allowed}
    data: dict[str, Any] = {}

    for field in ("shop_id", "payment_account_id"):
        try:
            data[field] = positive_integer(body.get(field), field)
        except ValueError as exc:
            errors[field] = str(exc)
    try:
        data["fulfillment"] = one_of(
            body.get("fulfillment"), "fulfillment", {"pickup", "delivery"}
        )
    except ValueError as exc:
        errors["fulfillment"] = str(exc)
    for field, limit in (("delivery_location", 500), ("remark", 2000)):
        try:
            data[field] = optional_string(body.get(field), field, max_length=limit)
        except ValueError as exc:
            errors[field] = str(exc)

    raw_items = body.get("items")
    items: list[dict[str, int]] = []
    if not isinstance(raw_items, list) or not raw_items:
        errors["items"] = "items must contain at least one menu item"
    else:
        seen: set[int] = set()
        for index, raw_item in enumerate(raw_items):
            if not isinstance(raw_item, dict):
                errors[f"items.{index}"] = "Each item must be an object"
                continue
            try:
                menu_id = positive_integer(raw_item.get("menu_id"), "menu_id")
                quantity = positive_integer(raw_item.get("quantity"), "quantity")
                if menu_id in seen:
                    raise ValueError("menu_id must not be duplicated")
                seen.add(menu_id)
                items.append({"menu_id": menu_id, "quantity": quantity})
            except ValueError as exc:
                errors[f"items.{index}"] = str(exc)
    data["items"] = items

    if data.get("fulfillment") == "delivery" and not data.get("delivery_location"):
        errors["delivery_location"] = "delivery_location is required for delivery"
    if errors:
        raise ValidationError(errors=errors)
    return data
