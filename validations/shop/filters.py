"""Validated list filters for the shop portal."""

from typing import Any

from validations.shared.filters import POSITIVE_INTEGER_FILTER, query_boolean, query_string, validate_query_filters


def validate_menu_filters(query: Any) -> dict:
    """Menus support search, availability, and genre filters."""
    return validate_query_filters(
        query,
        {
            "search": query_string,
            "is_available": query_boolean,
            "genre_id": POSITIVE_INTEGER_FILTER,
        },
    )
