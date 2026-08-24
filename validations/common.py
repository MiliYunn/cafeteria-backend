"""Reusable parameter-level validators."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from urllib.parse import urlparse

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


def optional_string(value: Any, field: str, *, max_length: int = 255) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    clean = value.strip()
    if len(clean) > max_length:
        raise ValueError(f"{field} must not exceed {max_length} characters")
    return clean or None


def boolean_value(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be a boolean")
    return value


def nullable_positive_integer(value: Any, field: str) -> int | None:
    if value is None:
        return None
    return positive_integer(value, field)


def valid_url(value: Any, field: str) -> str | None:
    clean = optional_string(value, field, max_length=500)
    if clean is None:
        return None
    parsed = urlparse(clean)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{field} must be a valid HTTP or HTTPS URL")
    return clean


def iso_datetime(value: Any, field: str) -> datetime | None:
    clean = optional_string(value, field, max_length=40)
    if clean is None:
        return None
    try:
        return datetime.fromisoformat(clean.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError as exc:
        raise ValueError(f"{field} must use ISO date-time format") from exc


def validate_pagination(page: Any, per_page: Any) -> tuple[int, int]:
    errors: dict[str, str] = {}
    try:
        clean_page = positive_integer(page or 1, "page")
    except ValueError as exc:
        errors["page"] = str(exc)
        clean_page = 1
    try:
        clean_per_page = positive_integer(per_page or 20, "per_page")
        if clean_per_page > 100:
            raise ValueError("per_page must not exceed 100")
    except ValueError as exc:
        errors["per_page"] = str(exc)
        clean_per_page = 20
    if errors:
        from validations.exceptions import ValidationError

        raise ValidationError(errors=errors)
    return clean_page, clean_per_page


def require_json_object(payload: Any) -> dict[str, Any]:
    from validations.exceptions import ValidationError

    if not isinstance(payload, dict):
        raise ValidationError(errors={"body": "A JSON object is required"})
    return payload


def require_update_fields(data: dict[str, Any]) -> dict[str, Any]:
    from validations.exceptions import ValidationError

    if not data:
        raise ValidationError(errors={"body": "At least one field is required"})
    return data


def validate_resource_payload(
    payload: Any,
    rules: dict[str, Any],
    *,
    required: set[str] | None = None,
    defaults: dict[str, Any] | None = None,
    partial: bool = False,
) -> dict[str, Any]:
    from validations.exceptions import ValidationError

    body = require_json_object(payload)
    errors: dict[str, str] = {}
    data: dict[str, Any] = {}
    unknown = set(body) - set(rules)
    for field in sorted(unknown):
        errors[field] = f"{field} is not allowed"
    for field, rule in rules.items():
        if field not in body:
            if not partial and required and field in required:
                errors[field] = f"{field} is required"
            elif not partial and defaults and field in defaults:
                data[field] = defaults[field]
            continue
        try:
            data[field] = rule(body[field], field)
        except ValueError as exc:
            errors[field] = str(exc)
    if errors:
        raise ValidationError(errors=errors)
    if partial:
        require_update_fields(data)
    return data
