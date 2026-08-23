"""Common model serialization helpers."""

from __future__ import annotations

from typing import Any


class SerializableMixin:
    def to_dict(self, *, exclude: set[str] | None = None) -> dict[str, Any]:
        excluded = exclude or set()
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in excluded
        }

