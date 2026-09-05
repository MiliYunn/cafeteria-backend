from datetime import datetime, time, timedelta
from importlib import import_module
from io import StringIO

import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy.dialects.mysql import TIME, dialect

from helpers.jwt import create_access_token
from models.shop import Shop
from services.admin.shop_service import ShopService
from services.shared.token_service import TokenService
from validations.admin.shop import validate_shop
from validations.shared.exceptions import ValidationError
from validations.shared.fields import clock_time


@pytest.mark.parametrize("value, expected", [
    ("08:30", time(8, 30)), ("08:30:45", time(8, 30, 45)),
    ("00:00:00", time(0)), ("23:59:59", time(23, 59, 59)),
    (None, None), ("", None), (" 08:30 ", time(8, 30)),
])
def test_clock_time_accepts_valid_local_times(value, expected):
    assert clock_time(value, "open_at") == expected


@pytest.mark.parametrize("value", [
    "2026-08-29T08:30:00", "08:30Z", "08:30:00+08:00", "8:30", "0830",
    "24:00", "12:60", "12:30:60", "-01:00", "08:30:00.1", "08:30 AM", 830, True,
])
def test_shop_time_invalid_values_have_field_errors(value):
    with pytest.raises(ValidationError) as caught:
        validate_shop({"open_at": value, "close_at": value}, partial=True)
    assert set(caught.value.errors) == {"open_at", "close_at"}


def test_overnight_hours_and_partial_updates():
    assert validate_shop({"open_at": "22:00", "close_at": "02:00"}, partial=True) == {
        "open_at": time(22), "close_at": time(2),
    }
    assert validate_shop({"close_at": None}, partial=True) == {"close_at": None}
    assert "open_at" not in validate_shop({"name": "New name"}, partial=True)


def test_shop_category_ids_are_validated_and_deduplicated():
    assert validate_shop({"category_ids": [3, "2", 3]}, partial=True) == {
        "category_ids": [3, 2]
    }
    for invalid in ("1,2", [0], [True], [1.5]):
        with pytest.raises(ValidationError):
            validate_shop({"category_ids": invalid}, partial=True)


def test_shop_serialization_handles_time_and_keeps_timestamps(app):
    created = datetime(2026, 8, 29, 12, 0)
    shop = Shop(id=1, open_at=time(0), close_at=time(23, 59, 59), created_at=created, password="hash")
    data = shop.to_dict(exclude={"password"})
    assert data["open_at"] == "00:00:00"
    assert data["close_at"] == "23:59:59"
    assert data["created_at"] == created
    assert "password" not in data
    assert app.json.loads(app.json.dumps(data))["open_at"] == "00:00:00"


def test_time_storage_round_trip_and_mysql_driver_conversion():
    assert isinstance(Shop.__table__.c.open_at.type, sa.Time)
    assert isinstance(Shop.__table__.c.close_at.type, sa.Time)
    engine = sa.create_engine("sqlite:///:memory:")
    table = sa.Table("hours", sa.MetaData(), sa.Column("open_at", Shop.__table__.c.open_at.type), sa.Column("close_at", Shop.__table__.c.close_at.type))
    table.create(engine)
    with engine.begin() as connection:
        connection.execute(table.insert().values(open_at=time(8, 30, 15), close_at=None))
        result = connection.execute(sa.select(table)).one()
        assert result.open_at == time(8, 30, 15)
        assert result.close_at is None
    engine.dispose()
    # PyMySQL returns timedelta for TIME; SQLAlchemy normalizes it to time.
    assert TIME().result_processor(dialect(), None)(timedelta(hours=8, minutes=30)) == time(8, 30)


def test_admin_shop_update_returns_time_only_json(app, client, monkeypatch):
    monkeypatch.setattr(TokenService, "is_revoked", lambda _jti: False)
    def update(_id, data):
        assert data == {"open_at": time(8, 30), "close_at": time(21)}
        return Shop(id=_id, **data).to_dict(exclude={"password"})
    monkeypatch.setattr(ShopService, "update", update)
    token = create_access_token(1, "admin", app.config["SETTINGS"].jwt_secret, 60)
    response = client.put("/cafeteria/admin/shops/1", json={"open_at": "08:30", "close_at": "21:00"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json["data"]["open_at"] == "08:30:00"
    assert response.json["data"]["close_at"] == "21:00:00"


def test_shop_migration_sql_is_focused_and_documents_lossy_downgrade():
    revision = import_module("database.migrations.versions.032_shops_time_only")
    for action, expected_type in ((revision.upgrade, "TIME"), (revision.downgrade, "DATETIME")):
        output = StringIO()
        context = MigrationContext.configure(dialect_name="mysql", opts={"as_sql": True, "output_buffer": output})
        with Operations.context(context):
            action()
        sql = output.getvalue()
        for column in ("open_at", "close_at"):
            assert (
                f"ALTER TABLE shops MODIFY {column} {expected_type} NULL" in sql
                or f"ALTER TABLE shops CHANGE {column} {column} {expected_type} NULL" in sql
            )
        assert "DROP TABLE" not in sql
        if action == revision.downgrade:
            assert "1970-01-01" in sql
            assert "updated_at = updated_at" in sql
