"""Consistent JSON response helpers."""

from __future__ import annotations

from typing import Any

from flask import jsonify


def success_response(data: Any = None, message: str = "OK", status_code: int = 200):
    payload = {"success": True, "message": message}
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status_code


def paginated_response(data: list[Any], pagination: dict[str, Any], message: str = "OK"):
    return jsonify(
        {
            "success": True,
            "message": message,
            "data": data,
            "pagination": pagination,
        }
    ), 200


def error_response(message: str, status_code: int = 400, errors: Any = None):
    payload = {"success": False, "message": message}
    if errors is not None:
        payload["errors"] = errors
    return jsonify(payload), status_code
