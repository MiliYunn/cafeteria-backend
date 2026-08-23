"""Validation exception translated to JSON by the application layer."""

from typing import Any


class ValidationError(Exception):
    def __init__(
        self,
        message: str = "Validation failed",
        errors: dict[str, Any] | None = None,
        status_code: int = 422,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.errors = errors or {}
        self.status_code = status_code

