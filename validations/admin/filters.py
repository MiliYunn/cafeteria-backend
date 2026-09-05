"""Validated filter parameters for admin collection endpoints."""

from typing import Any

from validations.shared.filters import (
    POSITIVE_INTEGER_FILTER,
    query_boolean,
    query_string,
    validate_query_filters,
)
from validations.shared.fields import one_of
from validations.admin.payment_method import PAYMENT_METHOD_TYPES
from validations.admin.shop_staff import SHOP_STAFF_ROLES


def validate_role_filters(query: Any) -> dict:
    """Roles support: search (name) and is_active (boolean)."""

    return validate_query_filters(
        query,
        {"search": query_string, "is_active": query_boolean},
    )


def validate_category_filters(query: Any) -> dict:
    """Categories support: search (name/description) and is_active."""

    return validate_query_filters(
        query,
        {"search": query_string, "is_active": query_boolean},
    )


def validate_genre_filters(query: Any) -> dict:
    """Genres support: search (name) and is_active."""

    return validate_query_filters(
        query,
        {"search": query_string, "is_active": query_boolean},
    )


def validate_shop_filters(query: Any) -> dict:
    """Shops support: search (name/email/location/description) and is_active."""

    return validate_query_filters(
        query,
        {"search": query_string, "is_active": query_boolean},
    )


def validate_shop_staff_filters(query: Any) -> dict:
    """Shop staff support: search (name/email/phone), status, and role."""

    return validate_query_filters(
        query,
        {
            "search": query_string,
            "is_active": query_boolean,
            "role": lambda value, field: one_of(value, field, SHOP_STAFF_ROLES),
        },
    )


def validate_user_filters(query: Any) -> dict:
    """Users support search, status, role, department, and type filters."""

    return validate_query_filters(
        query,
        {
            "search": query_string,
            "is_active": query_boolean,
            "role_id": POSITIVE_INTEGER_FILTER,
            "department_id": POSITIVE_INTEGER_FILTER,
            "type": query_string,
        },
    )


def validate_payment_method_filters(query: Any) -> dict:
    """Payment methods support search, status, and type filters."""

    return validate_query_filters(
        query,
        {
            "search": query_string,
            "is_active": query_boolean,
            "type": lambda value, field: one_of(value, field, PAYMENT_METHOD_TYPES),
        },
    )


def validate_payment_account_filters(query: Any) -> dict:
    """Payment accounts support search, status, and payment-method filters."""

    return validate_query_filters(
        query,
        {
            "search": query_string,
            "is_active": query_boolean,
            "payment_method_id": POSITIVE_INTEGER_FILTER,
        },
    )
