from unittest.mock import patch


def test_shop_order_routes_are_registered(app):
    routes = {
        (rule.rule, method)
        for rule in app.url_map.iter_rules()
        for method in rule.methods - {"HEAD", "OPTIONS"}
    }
    assert {
        ("/cafeteria/shop/orders", "GET"),
        ("/cafeteria/shop/orders/<int:order_id>", "GET"),
        ("/cafeteria/shop/orders/<int:order_id>/status", "PUT"),
    } <= routes


def test_shop_orders_require_shop_login(client):
    assert client.get("/cafeteria/shop/orders").status_code == 401
    assert client.get("/cafeteria/shop/orders/1").status_code == 401
    assert client.put("/cafeteria/shop/orders/1/status", json={"status": "confirmed"}).status_code == 401


def test_shop_order_list_is_scoped_to_authenticated_shop(client):
    with (
        patch("middlewares.jwt_auth.decode_access_token", return_value={"sub": "7", "role": "shop", "type": "access", "jti": "test"}),
        patch("middlewares.jwt_auth.TokenService.is_revoked", return_value=False),
        patch("controllers.shop.order_controller.ShopOrderService.list", return_value={"items": [], "pagination": {"page": 1, "per_page": 20, "total": 0, "total_pages": 0, "has_next": False, "has_previous": False}}) as listing,
    ):
        response = client.get("/cafeteria/shop/orders", headers={"Authorization": "Bearer token"})

    assert response.status_code == 200
    assert listing.call_args.args[0] == 7
