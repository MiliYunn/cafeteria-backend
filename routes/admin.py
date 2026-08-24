"""Admin portal endpoint registration only."""

from flask import Blueprint

from controllers.auth_controller import admin_login, logout
from controllers.category_controller import category_options, create_category, delete_category, get_category, list_categories, update_category
from controllers.genre_controller import create_genre, delete_genre, genre_options, get_genre, list_genres, update_genre
from controllers.payment_account_controller import create_payment_account, delete_payment_account, get_payment_account, list_payment_accounts, update_payment_account
from controllers.payment_method_controller import create_payment_method, delete_payment_method, get_payment_method, list_payment_methods, payment_method_options, update_payment_method
from controllers.role_controller import create_role, delete_role, get_role, list_roles, role_options, update_role
from controllers.shop_controller import create_shop, delete_shop, get_shop, list_shops, update_shop
from controllers.shop_staff_controller import create_shop_staff, delete_shop_staff, get_shop_staff, list_shop_staffs, update_shop_staff
from controllers.user_controller import create_user, delete_user, get_user, list_users, update_user
from middlewares.jwt_auth import jwt_required
from middlewares.rate_limit import admin_rate_limit, limiter

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")
admin_only = jwt_required({"admin"})
admin_bp.post("/auth/login")(limiter.limit(admin_rate_limit)(admin_login))
admin_bp.post("/auth/logout")(limiter.limit(admin_rate_limit)(admin_only(logout)))


def register_admin_route(rule: str, methods: list[str], handler) -> None:
    admin_bp.add_url_rule(
        rule,
        view_func=limiter.limit(admin_rate_limit)(admin_only(handler)),
        methods=methods,
    )


register_admin_route("/roles", ["GET"], list_roles)
register_admin_route("/roles", ["POST"], create_role)
register_admin_route("/roles/<int:role_id>", ["GET"], get_role)
register_admin_route("/roles/<int:role_id>", ["PUT"], update_role)
register_admin_route("/roles/<int:role_id>", ["DELETE"], delete_role)
register_admin_route("/role-options", ["GET"], role_options)

register_admin_route("/users", ["GET"], list_users)
register_admin_route("/users", ["POST"], create_user)
register_admin_route("/users/<int:user_id>", ["GET"], get_user)
register_admin_route("/users/<int:user_id>", ["PUT"], update_user)
register_admin_route("/users/<int:user_id>", ["DELETE"], delete_user)

register_admin_route("/categories", ["GET"], list_categories)
register_admin_route("/categories", ["POST"], create_category)
register_admin_route("/categories/<int:category_id>", ["GET"], get_category)
register_admin_route("/categories/<int:category_id>", ["PUT"], update_category)
register_admin_route("/categories/<int:category_id>", ["DELETE"], delete_category)
register_admin_route("/category-options", ["GET"], category_options)

register_admin_route("/genres", ["GET"], list_genres)
register_admin_route("/genres", ["POST"], create_genre)
register_admin_route("/genres/<int:genre_id>", ["GET"], get_genre)
register_admin_route("/genres/<int:genre_id>", ["PUT"], update_genre)
register_admin_route("/genres/<int:genre_id>", ["DELETE"], delete_genre)
register_admin_route("/genre-options", ["GET"], genre_options)

register_admin_route("/payment-methods", ["GET"], list_payment_methods)
register_admin_route("/payment-methods", ["POST"], create_payment_method)
register_admin_route("/payment-methods/<int:method_id>", ["GET"], get_payment_method)
register_admin_route("/payment-methods/<int:method_id>", ["PUT"], update_payment_method)
register_admin_route("/payment-methods/<int:method_id>", ["DELETE"], delete_payment_method)
register_admin_route("/payment-method-options", ["GET"], payment_method_options)

register_admin_route("/shops", ["GET"], list_shops)
register_admin_route("/shops", ["POST"], create_shop)
register_admin_route("/shops/<int:shop_id>", ["GET"], get_shop)
register_admin_route("/shops/<int:shop_id>", ["PUT"], update_shop)
register_admin_route("/shops/<int:shop_id>", ["DELETE"], delete_shop)

register_admin_route("/shops/<int:shop_id>/staffs", ["GET"], list_shop_staffs)
register_admin_route("/shops/<int:shop_id>/staffs", ["POST"], create_shop_staff)
register_admin_route("/shops/<int:shop_id>/staffs/<int:staff_id>", ["GET"], get_shop_staff)
register_admin_route("/shops/<int:shop_id>/staffs/<int:staff_id>", ["PUT"], update_shop_staff)
register_admin_route("/shops/<int:shop_id>/staffs/<int:staff_id>", ["DELETE"], delete_shop_staff)

register_admin_route("/shops/<int:shop_id>/payment-accounts", ["GET"], list_payment_accounts)
register_admin_route("/shops/<int:shop_id>/payment-accounts", ["POST"], create_payment_account)
register_admin_route("/shops/<int:shop_id>/payment-accounts/<int:account_id>", ["GET"], get_payment_account)
register_admin_route("/shops/<int:shop_id>/payment-accounts/<int:account_id>", ["PUT"], update_payment_account)
register_admin_route("/shops/<int:shop_id>/payment-accounts/<int:account_id>", ["DELETE"], delete_payment_account)
