"""Thin HTTP handlers for customer orders."""

from flask import g, request

from controllers.shared.pagination import pagination_parameters
from helpers.response import paginated_response, success_response
from services.api.order_service import OrderService
from validations.api.order import validate_order
from validations.shared.exceptions import ValidationError
from validations.shared.fields import positive_integer


def create_order():
    data = validate_order(request.get_json(silent=True))
    return success_response(
        OrderService.create(int(g.auth["sub"]), data), "Order placed", 201
    )


def list_orders():
    result = OrderService.list(int(g.auth["sub"]), *pagination_parameters())
    return paginated_response(result["items"], result["pagination"])


def get_order(order_id: int):
    try:
        clean_order_id = positive_integer(order_id, "order_id")
    except ValueError as exc:
        raise ValidationError(errors={"order_id": str(exc)}) from exc
    return success_response(OrderService.get(int(g.auth["sub"]), clean_order_id))
