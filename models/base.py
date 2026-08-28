"""Common model serialization helpers."""

from __future__ import annotations

from datetime import time
from typing import Any


class SerializableMixin:
    def to_dict(self, *, exclude: set[str] | None = None) -> dict[str, Any]:
        excluded = exclude or set()
        return {
            column.name: (
                value.isoformat(timespec="seconds") if isinstance(value, time) else value
            )
            for column in self.__table__.columns
            if column.name not in excluded
            for value in (getattr(self, column.name),)
        }
