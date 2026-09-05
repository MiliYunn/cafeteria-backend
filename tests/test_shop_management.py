from decimal import Decimal

import pytest
from werkzeug.datastructures import MultiDict

from validations.shared.exceptions import ValidationError
from validations.shop.filters import validate_menu_filters
from validations.shop.menu import validate_menu
from validations.shop.settings import validate_shop_settings
from validations.admin.filters import validate_shop_staff_filters
from validations.admin.shop_staff import validate_shop_staff


def test_shop_management_routes_are_registered(app):
    routes = {(rule.rule, method) for rule in app.url_map.iter_rules() for method in rule.methods - {"HEAD", "OPTIONS"}}
    assert {
        ("/cafeteria/shop/menus", "GET"),
        ("/cafeteria/shop/menus", "POST"),
        ("/cafeteria/shop/menus/<int:menu_id>", "GET"),
        ("/cafeteria/shop/menus/<int:menu_id>", "PUT"),
        ("/cafeteria/shop/menus/<int:menu_id>", "DELETE"),
        ("/cafeteria/shop/genre-options", "GET"),
        ("/cafeteria/shop/payment-method-options", "GET"),
    } <= routes
    assert ("/cafeteria/shop/settings", "GET") in routes
    assert ("/cafeteria/shop/settings", "PUT") in routes


@pytest.mark.parametrize("path", [
    "/cafeteria/shop/menus", "/cafeteria/shop/staffs",
    "/cafeteria/shop/payment-accounts", "/cafeteria/shop/genre-options",
        "/cafeteria/shop/payment-method-options",
        "/cafeteria/shop/settings",
])
def test_shop_management_requires_shop_token(client, path):
    response = client.get(path)
    assert response.status_code == 401
    assert response.json["message"] == "Missing bearer token"


def test_shop_menu_payload_is_normalized():
    data = validate_menu({"genre_ids": ["2", 3, 2], "name": "  Nasi Lemak  ", "cost": "8.5", "is_available": True, "description": "  Coconut rice  ", "image": None})
    assert data == {"genre_ids": [2, 3], "name": "Nasi Lemak", "cost": Decimal("8.50"), "is_available": True, "description": "Coconut rice", "image": None}


def test_shop_menu_filters_are_explicit():
    assert validate_menu_filters(MultiDict({"search": "rice", "genre_id": "3", "is_available": "false"})) == {"search": "rice", "genre_id": 3, "is_available": False}
    with pytest.raises(ValidationError) as caught:
        validate_menu_filters(MultiDict({"cost": "5"}))
    assert caught.value.errors == {"cost": "cost is not an allowed filter"}


def test_shop_staff_role_is_required_and_validated():
    assert validate_shop_staff({"name": "Aye Aye", "role": "cashier"})["role"] == "cashier"
    with pytest.raises(ValidationError) as caught:
        validate_shop_staff({"name": "Aye Aye", "role": "pilot"})
    assert "role" in caught.value.errors


def test_shop_staff_list_supports_role_filter():
    assert validate_shop_staff_filters(MultiDict({"role": "cook"})) == {"role": "cook"}


def test_shop_settings_accept_time_only_values():
    settings = validate_shop_settings({"open_at": "08:30", "close_at": "21:45"})
    assert settings["open_at"].isoformat() == "08:30:00"
    assert settings["close_at"].isoformat() == "21:45:00"

    with pytest.raises(ValidationError) as caught:
        validate_shop_settings({"open_at": "tomorrow"})
    assert "open_at" in caught.value.errors
