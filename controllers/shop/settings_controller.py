"""Thin HTTP handlers for authenticated shop settings."""

from flask import g, request

from helpers.response import success_response
from services.shop.settings_service import ShopSettingsService
from validations.shop.settings import validate_shop_settings


def _shop_id() -> int:
    return int(g.auth["sub"])


def get_settings():
    return success_response(ShopSettingsService.get(_shop_id()), "Shop settings retrieved")


def update_settings():
    data = validate_shop_settings(request.get_json(silent=True))
    return success_response(ShopSettingsService.update(_shop_id(), data), "Shop settings updated")
