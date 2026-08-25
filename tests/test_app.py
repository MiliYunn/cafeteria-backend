from unittest.mock import patch

from extensions import db
from helpers.jwt import create_access_token


def test_health(client):
    response = client.get("/cafeteria/health")
    assert response.status_code == 200
    assert response.json == {"success": True, "message": "OK", "data": {"status": "healthy"}}


def test_all_erd_tables_are_registered(app):
    with app.app_context():
        assert set(db.metadata.tables) == {
            "roles", "users", "shops", "shop_staffs", "categories", "shop_categories",
            "genres", "menus", "payment_methods", "payment_accounts", "orders",
            "order_menus", "order_logs", "user_activities", "revoked_tokens",
        }


def test_every_table_has_timestamps(app):
    with app.app_context():
        for table in db.metadata.tables.values():
            assert "created_at" in table.columns, table.name
            assert "updated_at" in table.columns, table.name


def test_payment_accounts_belong_to_shops(app):
    with app.app_context():
        table = db.metadata.tables["payment_accounts"]
        assert not table.columns.shop_id.nullable
        assert {foreign_key.target_fullname for foreign_key in table.columns.shop_id.foreign_keys} == {
            "shops.id"
        }


def test_admin_route_requires_token(client):
    response = client.get("/cafeteria/admin/users")
    assert response.status_code == 401
    assert response.json["message"] == "Missing bearer token"


def test_versioned_routes_are_not_registered(client):
    assert client.get("/api/v1/health").status_code == 404
    assert client.get("/health").status_code == 404


def test_portal_login_routes_are_registered(app):
    rules = {str(rule) for rule in app.url_map.iter_rules()}
    assert "/cafeteria/api/auth/login" in rules
    assert "/cafeteria/admin/auth/login" in rules


def test_admin_auth_profile_and_revoke_routes_are_registered(app):
    routes = {
        (rule.rule, method)
        for rule in app.url_map.iter_rules()
        for method in rule.methods - {"HEAD", "OPTIONS"}
    }
    assert ("/cafeteria/admin/auth/profile", "GET") in routes
    assert ("/cafeteria/admin/auth/revoke-token", "POST") in routes
    assert ("/cafeteria/admin/auth/refresh-token", "POST") in routes


def test_admin_auth_profile_and_revoke_require_token(client):
    assert client.get("/cafeteria/admin/auth/profile").status_code == 401
    assert client.post("/cafeteria/admin/auth/revoke-token").status_code == 401


def test_admin_refresh_token_validates_payload(client):
    response = client.post("/cafeteria/admin/auth/refresh-token", json={})
    assert response.status_code == 422
    assert response.json["errors"] == {
        "refresh_token": "refresh_token is required",
    }


def test_admin_refresh_token_returns_rotated_pair(client):
    refreshed = {
        "access_token": "new-access-token",
        "refresh_token": "new-refresh-token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "refresh_expires_in": 604800,
    }
    with patch(
        "controllers.admin.auth_controller.AdminAuthService.refresh",
        return_value=refreshed,
    ) as refresh:
        response = client.post(
            "/cafeteria/admin/auth/refresh-token",
            json={"refresh_token": "old-refresh-token"},
        )

    assert response.status_code == 200
    assert response.json["data"] == refreshed
    refresh.assert_called_once()


def test_admin_revoke_accepts_its_expired_bearer_token(app, client):
    token = create_access_token(
        7,
        "admin",
        app.config["SETTINGS"].jwt_secret,
        expires_minutes=-1,
    )
    headers = {"Authorization": f"Bearer {token}"}

    with (
        patch("middlewares.jwt_auth.TokenService.is_revoked", return_value=False),
        patch("controllers.admin.auth_controller.AdminAuthService.logout") as revoke,
    ):
        response = client.post(
            "/cafeteria/admin/auth/revoke-token",
            headers=headers,
        )

    assert response.status_code == 200
    assert response.json["message"] == "Token revoked successfully"
    revoke.assert_called_once()


def test_portal_blueprints_use_cafeteria_root(app):
    assert "cafeteria.admin" in app.blueprints
    assert "cafeteria.api" in app.blueprints
    assert "cafeteria.shop" in app.blueprints


def test_student_login_validates_payload(client):
    response = client.post("/cafeteria/api/auth/login", json={})
    assert response.status_code == 422
    assert set(response.json["errors"]) == {"email", "password"}


def test_admin_login_validates_payload(client):
    response = client.post("/cafeteria/admin/auth/login", json={})
    assert response.status_code == 422
    assert set(response.json["errors"]) == {"email", "password"}


def test_admin_login_rejects_generic_login_field(client):
    response = client.post(
        "/cafeteria/admin/auth/login",
        json={"login": "admin", "password": "secret"},
    )
    assert response.status_code == 422
    assert set(response.json["errors"]) == {"email", "login"}


def test_student_logout_requires_token(client):
    response = client.post("/cafeteria/api/auth/logout")
    assert response.status_code == 401


def test_admin_logout_requires_token(client):
    response = client.post("/cafeteria/admin/auth/logout")
    assert response.status_code == 401
