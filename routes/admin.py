"""Admin portal endpoint registration only."""

from flask import Blueprint

from controllers.admin_controller import create_category, list_categories, list_users
from controllers.auth_controller import admin_login, logout
from middlewares.jwt_auth import jwt_required
from middlewares.rate_limit import admin_rate_limit, limiter

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")
admin_only = jwt_required({"admin"})
admin_bp.post("/auth/login")(limiter.limit(admin_rate_limit)(admin_login))
admin_bp.post("/auth/logout")(limiter.limit(admin_rate_limit)(admin_only(logout)))
admin_bp.get("/users")(limiter.limit(admin_rate_limit)(admin_only(list_users)))
admin_bp.get("/categories")(limiter.limit(admin_rate_limit)(admin_only(list_categories)))
admin_bp.post("/categories")(limiter.limit(admin_rate_limit)(admin_only(create_category)))
