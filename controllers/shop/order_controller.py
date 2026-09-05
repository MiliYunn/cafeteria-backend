"""Thin HTTP handlers for shop order management and pricing."""

from flask import g, request

from controllers.shared.pagination import pagination_parameters
from helpers.response import paginated_response, success_response
from services.shared.order_fee_service import OrderFeeService
from services.shop.order_service import ShopOrderService
from validations.shared.exceptions import ValidationError
from validations.shared.fields import positive_integer
from validations.shop.filters import validate_order_filters
from validations.shop.order import validate_order_status


def _shop_id() -> int:
    return int(g.auth["sub"])


def _order_id(value: int) -> int:
    try:
        return positive_integer(value, "order_id")
    except ValueError as exc:
        raise ValidationError(errors={"order_id": str(exc)}) from exc


def get_order_fees():
    return success_response(
        OrderFeeService.configuration(), "Order fee configuration retrieved"
    )


def list_orders():
    result = ShopOrderService.list(
        _shop_id(),
        *pagination_parameters(),
        validate_order_filters(request.args),
    )
    return paginated_response(result["items"], result["pagination"])


def get_order(order_id: int):
    return success_response(ShopOrderService.get(_shop_id(), _order_id(order_id)))


def update_order_status(order_id: int):
    data = validate_order_status(request.get_json(silent=True))
    return success_response(
        ShopOrderService.update_status(_shop_id(), _order_id(order_id), data["status"]),
        "Order status updated",
    )
