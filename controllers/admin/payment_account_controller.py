from flask import request

from controllers.shared.pagination import pagination_parameters
from helpers.response import paginated_response, success_response
from services.admin.payment_account_service import PaymentAccountService
from validations.admin.filters import validate_payment_account_filters
from validations.admin.payment_account import validate_payment_account


def list_payment_accounts(shop_id: int):
    result = PaymentAccountService.list(
        shop_id,
        *pagination_parameters(),
        validate_payment_account_filters(request.args),
    )
    return paginated_response(result["items"], result["pagination"])


def get_payment_account(shop_id: int, account_id: int):
    return success_response(PaymentAccountService.get(shop_id, account_id))


def create_payment_account(shop_id: int):
    data = validate_payment_account(request.get_json(silent=True))
    return success_response(PaymentAccountService.create(shop_id, data), "Payment account created", 201)


def update_payment_account(shop_id: int, account_id: int):
    data = validate_payment_account(request.get_json(silent=True), partial=True)
    return success_response(PaymentAccountService.update(shop_id, account_id, data), "Payment account updated")


def delete_payment_account(shop_id: int, account_id: int):
    PaymentAccountService.delete(shop_id, account_id)
    return success_response(message="Payment account deleted")
