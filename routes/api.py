"""Public API endpoint registration only."""

from flask import Blueprint

from controllers.api_controller import list_shop_menus, list_shops
from controllers.auth_controller import logout, student_login
from middlewares.jwt_auth import jwt_required
from middlewares.rate_limit import api_rate_limit, limiter

api_bp = Blueprint("api", __name__, url_prefix="/api")
api_bp.post("/auth/login")(limiter.limit(api_rate_limit)(student_login))
api_bp.post("/auth/logout")(
    limiter.limit(api_rate_limit)(jwt_required({"student"})(logout))
)
api_bp.get("/shops")(limiter.limit(api_rate_limit)(list_shops))
api_bp.get("/shops/<int:shop_id>/menus")(limiter.limit(api_rate_limit)(list_shop_menus))
