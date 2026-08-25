"""Shared database operations used by administrative services."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from sqlalchemy.exc import IntegrityError

from extensions import db
from validations.shared.exceptions import ValidationError


def get_record(model, record_id: int, resource_name: str):
    record = db.session.get(model, record_id)
    if record is None:
        raise ValidationError(f"{resource_name} not found", status_code=404)
    return record


def paginate_records(statement, page: int, per_page: int, serializer: Callable[[Any], dict]) -> dict:
    result = db.paginate(statement, page=page, per_page=per_page, error_out=False)
    return {
        "items": [serializer(item) for item in result.items],
        "pagination": {
            "page": result.page,
            "per_page": result.per_page,
            "total": result.total,
            "total_pages": result.pages,
            "has_next": result.has_next,
            "has_previous": result.has_prev,
        },
    }


def commit_record(record, conflict_message: str):
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ValidationError(conflict_message, status_code=409) from exc
    db.session.refresh(record)
    return record


def delete_record(record, conflict_message: str) -> None:
    db.session.delete(record)
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ValidationError(conflict_message, status_code=409) from exc
