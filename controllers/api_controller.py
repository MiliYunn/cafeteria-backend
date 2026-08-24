from controllers.common import pagination_parameters
from helpers.response import paginated_response, success_response
from services.catalog_service import CatalogService
from validations.common import positive_integer
from validations.exceptions import ValidationError


def health():
    return success_response({"status": "healthy"})


def list_shops():
    result = CatalogService.list_shops(*pagination_parameters())
    return paginated_response(result["items"], result["pagination"])


def list_shop_menus(shop_id: int):
    try:
        clean_shop_id = positive_integer(shop_id, "shop_id")
    except ValueError as exc:
        raise ValidationError(errors={"shop_id": str(exc)}) from exc
    result = CatalogService.list_shop_menus(clean_shop_id, *pagination_parameters())
    return paginated_response(result["items"], result["pagination"])
