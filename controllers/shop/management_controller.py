"""Shop-scoped staff and payment-account request handlers."""

from flask import g

from helpers.response import success_response
from services.admin.genre_service import GenreService
from services.admin.payment_method_service import PaymentMethodService

from controllers.admin.payment_account_controller import (
    create_payment_account, delete_payment_account, get_payment_account,
    list_payment_accounts, update_payment_account,
)
from controllers.admin.shop_staff_controller import (
    create_shop_staff, delete_shop_staff, get_shop_staff, list_shop_staffs,
    update_shop_staff,
)


def _shop_id() -> int:
    return int(g.auth["sub"])


def list_staff(): return list_shop_staffs(_shop_id())
def create_staff(): return create_shop_staff(_shop_id())
def get_staff(staff_id: int): return get_shop_staff(_shop_id(), staff_id)
def update_staff(staff_id: int): return update_shop_staff(_shop_id(), staff_id)
def delete_staff(staff_id: int): return delete_shop_staff(_shop_id(), staff_id)
def list_accounts(): return list_payment_accounts(_shop_id())
def create_account(): return create_payment_account(_shop_id())
def get_account(account_id: int): return get_payment_account(_shop_id(), account_id)
def update_account(account_id: int): return update_payment_account(_shop_id(), account_id)
def delete_account(account_id: int): return delete_payment_account(_shop_id(), account_id)
def genre_options(): return success_response(GenreService.options())
def payment_method_options(): return success_response(PaymentMethodService.options())
