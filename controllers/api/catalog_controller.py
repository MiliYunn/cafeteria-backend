from flask import request

from controllers.shared.pagination import pagination_parameters
from helpers.response import paginated_response, success_response
from services.api.catalog_service import CatalogService
from validations.shared.exceptions import ValidationError
from validations.shared.fields import positive_integer
from validations.api.filters import validate_menu_filters, validate_shop_filters


def list_shops():
    result = CatalogService.list_shops(
        *pagination_parameters(),
        validate_shop_filters(request.args),
    )
    return paginated_response(result["items"], result["pagination"])


def list_shop_categories():
    return success_response(
        CatalogService.list_categories(), "Shop categories retrieved"
    )


def list_shop_menus(shop_id: int):
    try:
        clean_shop_id = positive_integer(shop_id, "shop_id")
    except ValueError as exc:
        raise ValidationError(errors={"shop_id": str(exc)}) from exc
    result = CatalogService.list_shop_menus(
        clean_shop_id,
        *pagination_parameters(),
        validate_menu_filters(request.args),
    )
    return paginated_response(result["items"], result["pagination"])
