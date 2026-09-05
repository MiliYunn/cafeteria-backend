"""Generate and decrypt shop auto-login links without exposing credentials."""

from base64 import urlsafe_b64encode
from hashlib import sha256
from urllib.parse import urlencode, urlparse

from cryptography.fernet import Fernet, InvalidToken

from validations.shared.exceptions import ValidationError


def _cipher(secret: str) -> Fernet:
    return Fernet(urlsafe_b64encode(sha256(secret.encode("utf-8")).digest()))


def encrypt_value(value: str, secret: str) -> str:
    return _cipher(secret).encrypt(value.encode("utf-8")).decode("ascii")


def decrypt_value(value: str, secret: str) -> str:
    try:
        return _cipher(secret).decrypt(value.encode("ascii")).decode("utf-8")
    except (InvalidToken, UnicodeError, ValueError) as exc:
        raise ValidationError("Invalid shop login link", status_code=401) from exc


def build_login_url(domain_url: str, email: str, password: str, secret: str) -> str:
    base = domain_url.rstrip("/") + "/auth/login"
    return f"{base}?{urlencode({'ce': encrypt_value(email.lower(), secret), 'cp': encrypt_value(password, secret)})}"


def rebase_login_url(domain_url: str, login_url: str) -> str:
    query = urlparse(login_url).query
    return f"{domain_url.rstrip('/')}/auth/login?{query}"
