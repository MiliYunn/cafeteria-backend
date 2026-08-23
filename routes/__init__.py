"""Blueprint registration."""

from flask import Flask

from routes.admin import admin_bp
from routes.api import api_bp
from routes.health import health_bp


def register_routes(app: Flask) -> None:
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
