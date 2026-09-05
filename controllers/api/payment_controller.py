"""Thin handlers for customer-facing payment choices."""

from helpers.response import success_response
from services.api.payment_service import PaymentService
from validations.shared.exceptions import ValidationError
from validations.shared.fields import positive_integer


def list_payment_accounts(shop_id: int):
    try:
        clean_shop_id = positive_integer(shop_id, "shop_id")
    except ValueError as exc:
        raise ValidationError(errors={"shop_id": str(exc)}) from exc
    return success_response(PaymentService.list_for_shop(clean_shop_id))
