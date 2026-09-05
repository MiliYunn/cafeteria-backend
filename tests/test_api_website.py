from unittest.mock import patch

import pytest

from services.api.auth_service import ApiAuthService
from validations.api.order import validate_order
from validations.shared.exceptions import ValidationError


def test_website_routes_are_registered(app):
    routes = {
        (rule.rule, method)
        for rule in app.url_map.iter_rules()
        for method in rule.methods - {"HEAD", "OPTIONS"}
    }
    expected = {
        ("/cafeteria/api/auth/profile", "GET"),
        ("/cafeteria/api/auth/profile", "PUT"),
        ("/cafeteria/api/shops", "GET"),
        ("/cafeteria/api/shops/<int:shop_id>/menus", "GET"),
        ("/cafeteria/api/shops/<int:shop_id>/payment-accounts", "GET"),
        ("/cafeteria/api/orders", "GET"),
        ("/cafeteria/api/orders", "POST"),
        ("/cafeteria/api/orders/<int:order_id>", "GET"),
    }
    assert expected <= routes


@pytest.mark.parametrize(
    "method,url",
    [
        ("get", "/cafeteria/api/auth/profile"),
        ("get", "/cafeteria/api/shops"),
        ("get", "/cafeteria/api/shops/1/menus"),
        ("get", "/cafeteria/api/shops/1/payment-accounts"),
        ("get", "/cafeteria/api/orders"),
        ("post", "/cafeteria/api/orders"),
    ],
)
def test_website_routes_require_login(client, method, url):
    assert getattr(client, method)(url).status_code == 401


def test_website_login_uses_one_day_access_token(client):
    login_result = {
        "access_token": "access-token",
        "token_type": "Bearer",
        "expires_in": 86400,
        "role": "student",
        "user": {"id": 1, "email": "st000001@gmail.com"},
    }
    with patch(
        "controllers.api.auth_controller.ApiAuthService.login",
        return_value=login_result,
    ) as login:
        response = client.post(
            "/cafeteria/api/auth/login",
            json={"email": "st000001@gmail.com", "password": "Student@123"},
        )

    assert response.status_code == 200
    assert response.json["data"]["expires_in"] == 86400
    assert login.call_args.kwargs["expires_minutes"] == 1440


def test_website_login_allows_students_and_staff_only():
    with patch("services.api.auth_service.AuthService.login", return_value={}) as login:
        ApiAuthService.login(
            "person@example.com",
            "password",
            jwt_secret="secret",
            expires_minutes=1440,
        )

    assert login.call_args.kwargs["allowed_roles"] == {"student", "staff"}
    assert login.call_args.kwargs["email_only"] is True


def test_delivery_order_requires_an_address():
    with pytest.raises(ValidationError) as caught:
        validate_order(
            {
                "shop_id": 1,
                "payment_account_id": 1,
                "fulfillment": "delivery",
                "items": [{"menu_id": 1, "quantity": 1}],
            }
        )

    assert caught.value.errors["delivery_location"] == (
        "delivery_location is required for delivery"
    )


def test_pickup_order_does_not_require_an_address():
    result = validate_order(
        {
            "shop_id": 1,
            "payment_account_id": 1,
            "fulfillment": "pickup",
            "items": [{"menu_id": 1, "quantity": 2}],
        }
    )

    assert result["delivery_location"] is None
