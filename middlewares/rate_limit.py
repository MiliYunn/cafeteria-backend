"""Central rate-limit extension and named policies."""

from flask import current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")


def api_rate_limit() -> str:
    return f"{current_app.config['SETTINGS'].rate_api_per_min} per minute"


def admin_rate_limit() -> str:
    return f"{current_app.config['SETTINGS'].rate_admin_per_min} per minute"

