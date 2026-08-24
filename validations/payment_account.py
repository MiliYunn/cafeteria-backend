from typing import Any

from validations.common import boolean_value, positive_integer, required_string, valid_url, validate_resource_payload

RULES = {
    "payment_method_id": positive_integer,
    "account_holder_name": lambda value, field: required_string(value, field, max_length=255),
    "account_number": lambda value, field: required_string(value, field, max_length=100),
    "is_active": boolean_value,
    "image": valid_url,
}


def validate_payment_account(payload: Any, *, partial: bool = False) -> dict:
    return validate_resource_payload(
        payload,
        RULES,
        required={"payment_method_id", "account_holder_name", "account_number"},
        defaults={"is_active": True, "image": None},
        partial=partial,
    )
