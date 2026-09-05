from flask import current_app, g, request

from helpers.response import success_response
from services.shop.auth_service import ShopAuthService
from validations.shop.auth import validate_shop_link, validate_shop_refresh


def shop_login():
    data = validate_shop_link(request.get_json(silent=True))
    settings = current_app.config["SETTINGS"]
    result = ShopAuthService.login(
        data["ce"], data["cp"], secret=settings.shop_login_secret,
        jwt_secret=settings.jwt_secret, expires_minutes=settings.jwt_expires_minutes,
        refresh_expires_days=settings.jwt_refresh_expires_days,
    )
    return success_response(result, "Shop login successful")


def shop_profile():
    return success_response(ShopAuthService.profile(int(g.auth["sub"])), "Shop profile retrieved")


def shop_refresh_token():
    data = validate_shop_refresh(request.get_json(silent=True))
    settings = current_app.config["SETTINGS"]
    result = ShopAuthService.refresh(
        data["refresh_token"],
        jwt_secret=settings.jwt_secret,
        expires_minutes=settings.jwt_expires_minutes,
        refresh_expires_days=settings.jwt_refresh_expires_days,
    )
    return success_response(result, "Shop token refreshed successfully")
