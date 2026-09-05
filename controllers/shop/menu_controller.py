"""Thin HTTP handlers for shop-owned menu items."""

from flask import g, request

from controllers.shared.pagination import pagination_parameters
from helpers.response import paginated_response, success_response
from services.shop.menu_service import MenuService
from validations.shop.filters import validate_menu_filters
from validations.shop.menu import validate_menu


def _shop_id() -> int:
    return int(g.auth["sub"])


def list_menus():
    result = MenuService.list(_shop_id(), *pagination_parameters(), validate_menu_filters(request.args))
    return paginated_response(result["items"], result["pagination"])


def get_menu(menu_id: int):
    return success_response(MenuService.get(_shop_id(), menu_id))


def create_menu():
    data = validate_menu(request.get_json(silent=True))
    return success_response(MenuService.create(_shop_id(), data), "Menu item created", 201)


def update_menu(menu_id: int):
    data = validate_menu(request.get_json(silent=True), partial=True)
    return success_response(MenuService.update(_shop_id(), menu_id, data), "Menu item updated")


def delete_menu(menu_id: int):
    MenuService.delete(_shop_id(), menu_id)
    return success_response(message="Menu item deleted")
