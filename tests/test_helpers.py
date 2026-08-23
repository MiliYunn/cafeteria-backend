import jwt
import pytest

from helpers.hash import hash_password, verify_password
from helpers.jwt import create_access_token, decode_access_token
from validations.auth import validate_login
from validations.exceptions import ValidationError


def test_password_hash_round_trip():
    password_hash = hash_password("a-strong-password")
    assert verify_password("a-strong-password", password_hash)
    assert not verify_password("wrong-password", password_hash)


def test_access_token_round_trip():
    secret = "x" * 48
    token = create_access_token(7, "admin", secret, 60)
    payload = decode_access_token(token, secret)
    assert payload["sub"] == "7"
    assert payload["role"] == "admin"
    assert payload["jti"]


def test_invalid_login_payload_has_field_errors():
    with pytest.raises(ValidationError) as caught:
        validate_login({"login": "", "password": None})
    assert set(caught.value.errors) == {"login", "password"}


def test_token_rejects_wrong_secret():
    token = create_access_token(1, "user", "x" * 48, 60)
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(token, "y" * 48)
