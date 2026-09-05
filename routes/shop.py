"""Shop portal endpoint registration."""

from flask import Blueprint

from controllers.shop.auth_controller import shop_login, shop_profile, shop_refresh_token
from controllers.shop.management_controller import (
    create_account, create_staff, delete_account, delete_staff, get_account,
    get_staff, genre_options, list_accounts, list_staff, payment_method_options,
    update_account, update_staff,
)
from controllers.shop.menu_controller import create_menu, delete_menu, get_menu, list_menus, update_menu
from controllers.shop.settings_controller import get_settings, update_settings
from helpers.file_uploader import upload_file
from middlewares.jwt_auth import jwt_required
from middlewares.rate_limit import api_rate_limit, limiter

shop_bp = Blueprint("shop", __name__, url_prefix="/shop")
shop_bp.post("/auth/login")(limiter.limit(api_rate_limit)(shop_login))
shop_bp.post("/auth/refresh-token")(limiter.limit(api_rate_limit)(shop_refresh_token))
shop_bp.get("/auth/profile")(limiter.limit(api_rate_limit)(jwt_required({"shop"})(shop_profile)))


def register_shop_route(rule: str, methods: list[str], handler) -> None:
    shop_bp.add_url_rule(rule, view_func=limiter.limit(api_rate_limit)(jwt_required({"shop"})(handler)), methods=methods)


register_shop_route("/staffs", ["GET"], list_staff)
register_shop_route("/staffs", ["POST"], create_staff)
register_shop_route("/staffs/<int:staff_id>", ["GET"], get_staff)
register_shop_route("/staffs/<int:staff_id>", ["PUT"], update_staff)
register_shop_route("/staffs/<int:staff_id>", ["DELETE"], delete_staff)
register_shop_route("/payment-accounts", ["GET"], list_accounts)
register_shop_route("/payment-accounts", ["POST"], create_account)
register_shop_route("/payment-accounts/<int:account_id>", ["GET"], get_account)
register_shop_route("/payment-accounts/<int:account_id>", ["PUT"], update_account)
register_shop_route("/payment-accounts/<int:account_id>", ["DELETE"], delete_account)
register_shop_route("/genre-options", ["GET"], genre_options)
register_shop_route("/payment-method-options", ["GET"], payment_method_options)
register_shop_route("/menus", ["GET"], list_menus)
register_shop_route("/menus", ["POST"], create_menu)
register_shop_route("/menus/<int:menu_id>", ["GET"], get_menu)
register_shop_route("/menus/<int:menu_id>", ["PUT"], update_menu)
register_shop_route("/menus/<int:menu_id>", ["DELETE"], delete_menu)
register_shop_route("/uploads", ["POST"], upload_file)
register_shop_route("/settings", ["GET"], get_settings)
register_shop_route("/settings", ["PUT"], update_settings)
