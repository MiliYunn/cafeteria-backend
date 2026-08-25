from decimal import Decimal

import pytest
from sqlalchemy import select
from werkzeug.datastructures import MultiDict

from models.user import User
from services.shared.filter_service import apply_collection_filters
from validations.admin.filters import validate_user_filters
from validations.api.filters import validate_menu_filters
from validations.shared.exceptions import ValidationError


def test_admin_filters_convert_query_values():
    filters = validate_user_filters(
        MultiDict(
            {
                "page": "2",
                "per_page": "10",
                "search": "alice",
                "is_active": "false",
                "role_id": "3",
            }
        )
    )
    assert filters == {
        "search": "alice",
        "is_active": False,
        "role_id": 3,
    }


def test_unknown_and_invalid_filters_return_field_errors():
    with pytest.raises(ValidationError) as caught:
        validate_user_filters(MultiDict({"enabled": "yes", "role_id": "zero"}))
    assert set(caught.value.errors) == {"enabled", "role_id"}


def test_menu_price_filters_are_validated():
    filters = validate_menu_filters(
        MultiDict({"genre_id": "2", "min_cost": "5.50", "max_cost": "12"})
    )
    assert filters == {
        "genre_id": 2,
        "min_cost": Decimal("5.50"),
        "max_cost": Decimal("12"),
    }

    with pytest.raises(ValidationError) as caught:
        validate_menu_filters(MultiDict({"min_cost": "20", "max_cost": "10"}))
    assert "max_cost" in caught.value.errors


def test_collection_filters_use_bound_sql_parameters():
    statement = apply_collection_filters(
        select(User),
        {"search": "alice", "role_id": 3, "is_active": True},
        search_columns=(User.username, User.email, User.fullname),
        exact_columns={"role_id": User.role_id, "is_active": User.is_active},
    )
    compiled = statement.compile()
    assert "WHERE" in str(compiled)
    assert "alice" not in str(compiled)
    assert any(value == "%alice%" for value in compiled.params.values())
