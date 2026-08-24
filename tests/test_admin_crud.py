import pytest

from helpers.response import paginated_response
from validations.common import validate_pagination
from validations.exceptions import ValidationError
from validations.role import validate_role
from validations.user import validate_user


def test_all_admin_crud_routes_are_registered(app):
    routes = {
        (rule.rule, method)
        for rule in app.url_map.iter_rules()
        for method in rule.methods - {"HEAD", "OPTIONS"}
    }
    resources = {
        "roles": "role_id",
        "users": "user_id",
        "categories": "category_id",
        "genres": "genre_id",
        "payment-methods": "method_id",
        "shops": "shop_id",
    }
    for resource, identifier in resources.items():
        base = f"/api/admin/{resource}"
        detail = f"{base}/<int:{identifier}>"
        assert (base, "GET") in routes
        assert (base, "POST") in routes
        assert (detail, "GET") in routes
        assert (detail, "PUT") in routes
        assert (detail, "DELETE") in routes


def test_nested_shop_crud_routes_are_registered(app):
    routes = {
        (rule.rule, method)
        for rule in app.url_map.iter_rules()
        for method in rule.methods - {"HEAD", "OPTIONS"}
    }
    for resource, identifier in (("staffs", "staff_id"), ("payment-accounts", "account_id")):
        base = f"/api/admin/shops/<int:shop_id>/{resource}"
        detail = f"{base}/<int:{identifier}>"
        for method, path in (("GET", base), ("POST", base), ("GET", detail), ("PUT", detail), ("DELETE", detail)):
            assert (path, method) in routes


def test_option_routes_are_registered(app):
    rules = {rule.rule for rule in app.url_map.iter_rules()}
    assert {
        "/api/admin/role-options",
        "/api/admin/category-options",
        "/api/admin/genre-options",
        "/api/admin/payment-method-options",
    } <= rules


def test_paginated_response_shape(app):
    with app.app_context():
        response, status = paginated_response(
            [{"id": 1, "name": "Admin"}],
            {"page": 1, "per_page": 20, "total": 1, "total_pages": 1, "has_next": False, "has_previous": False},
        )
        payload = response.get_json()
    assert status == 200
    assert payload["data"] == [{"id": 1, "name": "Admin"}]
    assert payload["pagination"]["total"] == 1


def test_pagination_defaults_and_limit():
    assert validate_pagination(None, None) == (1, 20)
    with pytest.raises(ValidationError) as caught:
        validate_pagination("0", "101")
    assert set(caught.value.errors) == {"page", "per_page"}


def test_role_create_and_update_validation():
    assert validate_role({"name": "Manager"}) == {"name": "Manager", "is_active": True}
    assert validate_role({"is_active": False}, partial=True) == {"is_active": False}


def test_user_password_is_required_only_when_creating():
    base = {
        "username": "student01",
        "email": "student@example.com",
        "fullname": "Student One",
        "role_id": 3,
        "type": "student",
    }
    with pytest.raises(ValidationError):
        validate_user(base)
    assert validate_user({"fullname": "Updated Student"}, partial=True) == {"fullname": "Updated Student"}
