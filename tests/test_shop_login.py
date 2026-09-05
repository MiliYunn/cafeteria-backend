from urllib.parse import parse_qs, urlparse

from helpers.shop_login import build_login_url, decrypt_value


def test_shop_login_link_round_trip():
    secret = "test-secret-that-is-at-least-thirty-two-characters"
    url = build_login_url("http://localhost:5174/", "Shop@Example.com", "secret-pass", secret)
    parsed = urlparse(url)
    values = parse_qs(parsed.query)

    assert f"{parsed.scheme}://{parsed.netloc}{parsed.path}" == "http://localhost:5174/auth/login"
    assert decrypt_value(values["ce"][0], secret) == "shop@example.com"
    assert decrypt_value(values["cp"][0], secret) == "secret-pass"
