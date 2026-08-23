from helpers.response import success_response
from services.catalog_service import CatalogService
from validations.common import positive_integer
from validations.exceptions import ValidationError


def health():
    return success_response({"status": "healthy"})


def list_shops():
    return success_response(CatalogService.list_shops())


def list_shop_menus(shop_id: int):
    try:
        clean_shop_id = positive_integer(shop_id, "shop_id")
    except ValueError as exc:
        raise ValidationError(errors={"shop_id": str(exc)}) from exc
    return success_response(CatalogService.list_shop_menus(clean_shop_id))

