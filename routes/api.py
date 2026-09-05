"""Public API endpoint registration only."""

from flask import Blueprint

from controllers.api.auth_controller import student_login, student_logout
from controllers.api.catalog_controller import (
    list_shop_categories,
    list_shop_menus,
    list_shops,
)
from controllers.api.order_controller import (
    create_order,
    get_order,
    get_order_fees,
    list_orders,
)
from controllers.api.payment_controller import list_payment_accounts
from controllers.api.profile_controller import get_profile, update_profile
from middlewares.jwt_auth import jwt_required
from middlewares.rate_limit import api_rate_limit, limiter

api_bp = Blueprint("api", __name__, url_prefix="/api")
api_bp.post("/auth/login")(limiter.limit(api_rate_limit)(student_login))


def register_api_route(rule: str, methods: list[str], handler) -> None:
    api_bp.add_url_rule(
        rule,
        view_func=limiter.limit(api_rate_limit)(
            jwt_required({"student", "staff"})(handler)
        ),
        methods=methods,
    )


register_api_route("/auth/logout", ["POST"], student_logout)
register_api_route("/auth/profile", ["GET"], get_profile)
register_api_route("/auth/profile", ["PUT"], update_profile)
register_api_route("/shops", ["GET"], list_shops)
register_api_route("/category-options", ["GET"], list_shop_categories)
register_api_route("/shops/<int:shop_id>/menus", ["GET"], list_shop_menus)
register_api_route(
    "/shops/<int:shop_id>/payment-accounts", ["GET"], list_payment_accounts
)
register_api_route("/orders", ["GET"], list_orders)
register_api_route("/orders", ["POST"], create_order)
register_api_route("/order-fees", ["GET"], get_order_fees)
register_api_route("/orders/<int:order_id>", ["GET"], get_order)
