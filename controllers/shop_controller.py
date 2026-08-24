from flask import request

from controllers.common import pagination_parameters
from helpers.response import paginated_response, success_response
from services.shop_service import ShopService
from validations.shop import validate_shop


def list_shops():
    result = ShopService.list(*pagination_parameters())
    return paginated_response(result["items"], result["pagination"])


def get_shop(shop_id: int):
    return success_response(ShopService.get(shop_id))


def create_shop():
    return success_response(ShopService.create(validate_shop(request.get_json(silent=True))), "Shop created", 201)


def update_shop(shop_id: int):
    return success_response(ShopService.update(shop_id, validate_shop(request.get_json(silent=True), partial=True)), "Shop updated")


def delete_shop(shop_id: int):
    ShopService.delete(shop_id)
    return success_response(message="Shop deleted")
