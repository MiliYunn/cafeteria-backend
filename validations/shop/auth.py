from typing import Any

from validations.shared.fields import required_string, validate_resource_payload


def validate_shop_link(payload: Any) -> dict:
    return validate_resource_payload(
        payload,
        {
            "ce": lambda value, field: required_string(value, field, max_length=2048),
            "cp": lambda value, field: required_string(value, field, max_length=2048),
        },
        required={"ce", "cp"},
    )


def validate_shop_refresh(payload: Any) -> dict:
    return validate_resource_payload(
        payload,
        {
            "refresh_token": lambda value, field: required_string(
                value, field, max_length=4096
            )
        },
        required={"refresh_token"},
    )
