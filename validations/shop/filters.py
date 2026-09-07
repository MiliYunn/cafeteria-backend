"""Validated list filters for the shop portal."""

from datetime import date
from typing import Any

from validations.shared.filters import POSITIVE_INTEGER_FILTER, query_boolean, query_string, validate_query_filters

ORDER_STATUSES = {"pending", "confirmed", "preparing", "ready", "completed", "cancelled"}


def _order_status(value: Any, field: str) -> str:
    clean = query_string(value, field)
    if clean not in ORDER_STATUSES:
        raise ValueError(f"{field} must be one of: {', '.join(sorted(ORDER_STATUSES))}")
    return clean


def _fulfillment(value: Any, field: str) -> str:
    clean = query_string(value, field)
    if clean not in {"pickup", "delivery"}:
        raise ValueError(f"{field} must be one of: delivery, pickup")
    return clean


def _order_date(value: Any, field: str) -> date:
    clean = query_string(value, field)
    try:
        return date.fromisoformat(clean or "")
    except ValueError as exc:
        raise ValueError(f"{field} must use YYYY-MM-DD format") from exc


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


def validate_order_filters(query: Any) -> dict:
    """Order history supports explicit, developer-visible filter keys."""
    return validate_query_filters(
        query,
        {
            "order_code": query_string,
            "customer_name": query_string,
            "order_date": _order_date,
            "status": _order_status,
        },
    )
