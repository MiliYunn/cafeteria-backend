"""Health-check endpoint registration only."""

from flask import Blueprint

from controllers.api_controller import health

health_bp = Blueprint("health", __name__)
health_bp.get("/health")(health)
