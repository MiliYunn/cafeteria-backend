from flask import request

from controllers.common import pagination_parameters
from helpers.response import paginated_response, success_response
from services.payment_method_service import PaymentMethodService
from validations.payment_method import validate_payment_method


def list_payment_methods():
    result = PaymentMethodService.list(*pagination_parameters())
    return paginated_response(result["items"], result["pagination"])


def payment_method_options():
    return success_response(PaymentMethodService.options())


def get_payment_method(method_id: int):
    return success_response(PaymentMethodService.get(method_id))


def create_payment_method():
    data = validate_payment_method(request.get_json(silent=True))
    return success_response(PaymentMethodService.create(data), "Payment method created", 201)


def update_payment_method(method_id: int):
    data = validate_payment_method(request.get_json(silent=True), partial=True)
    return success_response(PaymentMethodService.update(method_id, data), "Payment method updated")


def delete_payment_method(method_id: int):
    PaymentMethodService.delete(method_id)
    return success_response(message="Payment method deleted")
