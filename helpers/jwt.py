"""JWT encoding and decoding."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import jwt


def create_access_token(user_id: int, role: str, secret: str, expires_minutes: int) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "jti": str(uuid4()),
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
        "type": "access",
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def create_refresh_token(user_id: int, role: str, secret: str, expires_days: int) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "jti": str(uuid4()),
        "role": role,
        "iat": now,
        "exp": now + timedelta(days=expires_days),
        "type": "refresh",
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def _decode_token(
    token: str,
    secret: str,
    *,
    expected_type: str,
    verify_expiration: bool,
) -> dict[str, Any]:
    payload = jwt.decode(
        token,
        secret,
        algorithms=["HS256"],
        options={"verify_exp": verify_expiration},
    )
    if payload.get("type") != expected_type:
        raise jwt.InvalidTokenError(f"Invalid {expected_type} token type")
    if not payload.get("jti") or not payload.get("sub") or payload.get("exp") is None:
        raise jwt.InvalidTokenError("Token is missing required claims")
    return payload


def decode_access_token(
    token: str,
    secret: str,
    *,
    verify_expiration: bool = True,
) -> dict[str, Any]:
    return _decode_token(
        token,
        secret,
        expected_type="access",
        verify_expiration=verify_expiration,
    )


def decode_refresh_token(token: str, secret: str) -> dict[str, Any]:
    return _decode_token(
        token,
        secret,
        expected_type="refresh",
        verify_expiration=True,
    )
