"""Reusable parameter-level validators."""

from __future__ import annotations

from typing import Any

from email_validator import EmailNotValidError, validate_email


def required_string(value: Any, field: str, *, min_length: int = 1, max_length: int = 255) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} is required")
    clean = value.strip()
    if not min_length <= len(clean) <= max_length:
        raise ValueError(f"{field} must be between {min_length} and {max_length} characters")
    return clean


def valid_email(value: Any, field: str = "email") -> str:
    email = required_string(value, field, max_length=255).lower()
    try:
        return validate_email(email, check_deliverability=False).normalized
    except EmailNotValidError as exc:
        raise ValueError(f"{field} must be a valid email address") from exc


def positive_integer(value: Any, field: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a positive integer")
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a positive integer") from exc
    if number < 1:
        raise ValueError(f"{field} must be a positive integer")
    return number

