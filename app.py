"""Flask application factory."""

from __future__ import annotations

from flask import Flask
from werkzeug.exceptions import HTTPException

from config import FlaskConfig, Settings
from extensions import db
from helpers.logging import configure_logging
from helpers.response import error_response
from middlewares.cors import configure_cors
from middlewares.rate_limit import limiter
from routes import register_routes
from validations.exceptions import ValidationError


def create_app(test_config: dict | None = None) -> Flask:
    settings = Settings.from_env()
    configure_logging(settings.log_level)

    app = Flask(__name__)
    app.config.from_object(FlaskConfig(settings))
    app.config["SETTINGS"] = settings
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    limiter.init_app(app)
    configure_cors(app, settings.allow_origins)
    register_routes(app)
    register_error_handlers(app)
    return app


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValidationError)
    def handle_validation_error(exc: ValidationError):
        return error_response(exc.message, exc.status_code, exc.errors)

    @app.errorhandler(429)
    def handle_rate_limit(_exc):
        return error_response("Rate limit exceeded", 429)

    @app.errorhandler(HTTPException)
    def handle_http_error(exc: HTTPException):
        return error_response(exc.description, exc.code or 500)

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc: Exception):
        app.logger.exception("Unhandled application error", exc_info=exc)
        return error_response("Internal server error", 500)

