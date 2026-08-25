"""Blueprint registration."""

from flask import Blueprint, Flask

from routes.admin import admin_bp
from routes.api import api_bp
from routes.health import health_bp
from routes.shop import shop_bp
from routes.uploads import uploads_bp

ROOT_PREFIX = "/cafeteria"
cafeteria_bp = Blueprint("cafeteria", __name__, url_prefix=ROOT_PREFIX)
cafeteria_bp.register_blueprint(health_bp)
cafeteria_bp.register_blueprint(uploads_bp)
cafeteria_bp.register_blueprint(api_bp)
cafeteria_bp.register_blueprint(admin_bp)
cafeteria_bp.register_blueprint(shop_bp)


def register_routes(app: Flask) -> None:
    app.register_blueprint(cafeteria_bp)
