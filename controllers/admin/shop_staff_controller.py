from flask import request

from controllers.shared.pagination import pagination_parameters
from helpers.response import paginated_response, success_response
from services.admin.shop_staff_service import ShopStaffService
from validations.admin.filters import validate_shop_staff_filters
from validations.admin.shop_staff import validate_shop_staff


def list_shop_staffs(shop_id: int):
    result = ShopStaffService.list(
        shop_id,
        *pagination_parameters(),
        validate_shop_staff_filters(request.args),
    )
    return paginated_response(result["items"], result["pagination"])


def get_shop_staff(shop_id: int, staff_id: int):
    return success_response(ShopStaffService.get(shop_id, staff_id))


def create_shop_staff(shop_id: int):
    data = validate_shop_staff(request.get_json(silent=True))
    return success_response(ShopStaffService.create(shop_id, data), "Shop staff created", 201)


def update_shop_staff(shop_id: int, staff_id: int):
    data = validate_shop_staff(request.get_json(silent=True), partial=True)
    return success_response(ShopStaffService.update(shop_id, staff_id, data), "Shop staff updated")


def delete_shop_staff(shop_id: int, staff_id: int):
    ShopStaffService.delete(shop_id, staff_id)
    return success_response(message="Shop staff deleted")
