from typing import Any

from validations.shared.fields import boolean_value, one_of, optional_string, required_string, valid_email, validate_resource_payload


SHOP_STAFF_ROLES = {
    "manager",
    "supervisor",
    "cashier",
    "cook",
    "server",
    "cleaner",
    "delivery",
    "kitchen_helper",
    "inventory_clerk",
    "staff",
}


def _optional_email(value: Any, field: str) -> str | None:
    if value is None or value == "":
        return None
    return valid_email(value, field)


RULES = {
    "name": lambda value, field: required_string(value, field, max_length=255),
    "role": lambda value, field: one_of(value, field, SHOP_STAFF_ROLES),
    "email": _optional_email,
    "phone": lambda value, field: optional_string(value, field, max_length=30),
    "is_active": boolean_value,
}


def validate_shop_staff(payload: Any, *, partial: bool = False) -> dict:
    return validate_resource_payload(payload, RULES, required={"name", "role"}, defaults={"email": None, "phone": None, "is_active": True}, partial=partial)
