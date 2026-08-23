"""JWT authentication and role authorization decorators."""

from __future__ import annotations

from functools import wraps

import jwt
from flask import current_app, g, request

from helpers.jwt import decode_access_token
from helpers.response import error_response
from services.token_service import TokenService


def jwt_required(roles: set[str] | None = None):
    def decorator(handler):
        @wraps(handler)
        def wrapped(*args, **kwargs):
            header = request.headers.get("Authorization", "")
            if not header.startswith("Bearer "):
                return error_response("Missing bearer token", 401)
            try:
                payload = decode_access_token(
                    header.removeprefix("Bearer ").strip(),
                    current_app.config["SETTINGS"].jwt_secret,
                )
            except jwt.ExpiredSignatureError:
                return error_response("Token has expired", 401)
            except jwt.InvalidTokenError:
                return error_response("Invalid token", 401)
            if TokenService.is_revoked(payload["jti"]):
                return error_response("Token has been revoked", 401)
            if roles and payload.get("role") not in roles:
                return error_response("Insufficient permissions", 403)
            g.auth = payload
            return handler(*args, **kwargs)

        return wrapped

    return decorator
