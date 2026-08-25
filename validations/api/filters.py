"""Validated filters for public API collection endpoints."""

from typing import Any

from validations.shared.filters import (
    POSITIVE_INTEGER_FILTER,
    query_decimal,
    query_string,
    validate_query_filters,
)


def validate_shop_filters(query: Any) -> dict:
    return validate_query_filters(query, {"search": query_string})


def validate_menu_filters(query: Any) -> dict:
    filters = validate_query_filters(
        query,
        {
            "search": query_string,
            "genre_id": POSITIVE_INTEGER_FILTER,
            "min_cost": query_decimal,
            "max_cost": query_decimal,
        },
    )
    if (
        "min_cost" in filters
        and "max_cost" in filters
        and filters["min_cost"] > filters["max_cost"]
    ):
        from validations.shared.exceptions import ValidationError

        raise ValidationError(
            errors={"max_cost": "max_cost must be greater than or equal to min_cost"}
        )
    return filters
