"""Common model serialization helpers."""

from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
from typing import Any

MALAYSIA_TIMEZONE = timezone(timedelta(hours=8))


def _serialize_value(value: Any) -> Any:
    if isinstance(value, datetime):
        # MySQL returns TIMESTAMP and DATETIME columns without tzinfo. The
        # database runs in Malaysia time, so attach the real offset before
        # sending the value to JavaScript. Otherwise Flask labels the naive
        # value as GMT and browsers add another eight hours.
        localized = (
            value.replace(tzinfo=MALAYSIA_TIMEZONE)
            if value.tzinfo is None
            else value.astimezone(MALAYSIA_TIMEZONE)
        )
        return localized.isoformat(timespec="seconds")
    if isinstance(value, time):
        return value.isoformat(timespec="seconds")
    return value


class SerializableMixin:
    def to_dict(self, *, exclude: set[str] | None = None) -> dict[str, Any]:
        excluded = exclude or set()
        return {
            column.name: _serialize_value(value)
            for column in self.__table__.columns
            if column.name not in excluded
            for value in (getattr(self, column.name),)
        }
