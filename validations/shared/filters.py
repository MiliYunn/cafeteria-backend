"""Reusable validation for collection query-string filters."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from decimal import Decimal, InvalidOperation
from typing import Any

from validations.shared.exceptions import ValidationError
from validations.shared.fields import optional_string, positive_integer

FilterRule = Callable[[Any, str], Any]


def query_string(value: Any, field: str) -> str | None:
    return optional_string(value, field, max_length=255)


def query_boolean(value: Any, field: str) -> bool:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be true or false")
    normalized = value.strip().lower()
    if normalized in {"true", "1"}:
        return True
    if normalized in {"false", "0"}:
        return False
    raise ValueError(f"{field} must be true or false")


def query_decimal(value: Any, field: str) -> Decimal:
    try:
        number = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a non-negative number") from exc
    if not number.is_finite() or number < 0:
        raise ValueError(f"{field} must be a non-negative number")
    return number


def validate_query_filters(
    query: Mapping[str, Any],
    rules: dict[str, FilterRule],
) -> dict[str, Any]:
    errors: dict[str, str] = {}
    filters: dict[str, Any] = {}
    allowed = {"page", "per_page", *rules}

    for field in sorted(set(query) - allowed):
        errors[field] = f"{field} is not an allowed filter"

    for field, rule in rules.items():
        if field not in query:
            continue
        try:
            value = rule(query.get(field), field)
            if value is not None:
                filters[field] = value
        except ValueError as exc:
            errors[field] = str(exc)

    if errors:
        raise ValidationError(errors=errors)
    return filters


POSITIVE_INTEGER_FILTER = positive_integer
