"""Composable SQLAlchemy filters for paginated collection queries."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from sqlalchemy import or_
from sqlalchemy.sql import ColumnElement, Select


def apply_collection_filters(
    statement: Select,
    filters: dict[str, Any],
    *,
    search_columns: Sequence[ColumnElement] = (),
    exact_columns: Mapping[str, ColumnElement] | None = None,
) -> Select:
    search = filters.get("search")
    if search and search_columns:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(*(column.ilike(pattern) for column in search_columns))
        )
    for name, column in (exact_columns or {}).items():
        if name in filters:
            statement = statement.where(column == filters[name])
    return statement
