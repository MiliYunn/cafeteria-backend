from extensions import db


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"success": True, "message": "OK", "data": {"status": "healthy"}}


def test_all_erd_tables_are_registered(app):
    with app.app_context():
        assert set(db.metadata.tables) == {
            "roles", "users", "shops", "shop_staffs", "categories", "shop_categories",
            "genres", "menus", "payment_methods", "payment_accounts", "orders",
            "order_menus", "order_logs", "user_activities", "revoked_tokens",
        }


def test_admin_route_requires_token(client):
    response = client.get("/api/admin/users")
    assert response.status_code == 401
    assert response.json["message"] == "Missing bearer token"


def test_versioned_routes_are_not_registered(client):
    assert client.get("/api/v1/health").status_code == 404


def test_portal_login_routes_are_registered(app):
    rules = {str(rule) for rule in app.url_map.iter_rules()}
    assert "/api/auth/login" in rules
    assert "/api/admin/auth/login" in rules


def test_student_login_validates_payload(client):
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 422
    assert set(response.json["errors"]) == {"login", "password"}


def test_admin_login_validates_payload(client):
    response = client.post("/api/admin/auth/login", json={})
    assert response.status_code == 422
    assert set(response.json["errors"]) == {"login", "password"}


def test_student_logout_requires_token(client):
    response = client.post("/api/auth/logout")
    assert response.status_code == 401


def test_admin_logout_requires_token(client):
    response = client.post("/api/admin/auth/logout")
    assert response.status_code == 401
