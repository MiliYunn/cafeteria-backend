from datetime import UTC, datetime

import jwt
from sqlalchemy import select

from extensions import db
from helpers.hash import verify_password
from helpers.jwt import create_access_token, create_refresh_token, decode_refresh_token
from helpers.shop_login import decrypt_value
from models.shop import Shop
from services.shared.token_service import TokenService
from validations.shared.exceptions import ValidationError


class ShopAuthService:
    @staticmethod
    def _token_pair(shop_id: int, *, jwt_secret: str, expires_minutes: int, refresh_expires_days: int) -> dict:
        return {
            "access_token": create_access_token(shop_id, "shop", jwt_secret, expires_minutes),
            "refresh_token": create_refresh_token(shop_id, "shop", jwt_secret, refresh_expires_days),
            "token_type": "Bearer",
            "expires_in": expires_minutes * 60,
            "refresh_expires_in": refresh_expires_days * 86400,
        }

    @staticmethod
    def login(ce: str, cp: str, *, secret: str, jwt_secret: str, expires_minutes: int, refresh_expires_days: int) -> dict:
        email = decrypt_value(ce, secret).lower()
        password = decrypt_value(cp, secret)
        shop = db.session.execute(select(Shop).where(Shop.email == email)).scalar_one_or_none()
        if shop is None or not shop.is_active or not verify_password(password, shop.password):
            raise ValidationError("Invalid shop login link", status_code=401)
        return {
            **ShopAuthService._token_pair(
                shop.id,
                jwt_secret=jwt_secret,
                expires_minutes=expires_minutes,
                refresh_expires_days=refresh_expires_days,
            ),
            "shop": shop.to_dict(exclude={"password", "login_url"}),
        }

    @staticmethod
    def refresh(refresh_token: str, *, jwt_secret: str, expires_minutes: int, refresh_expires_days: int) -> dict:
        try:
            payload = decode_refresh_token(refresh_token, jwt_secret)
            shop_id = int(payload["sub"])
        except jwt.ExpiredSignatureError as exc:
            raise ValidationError("Refresh token has expired", status_code=401) from exc
        except (jwt.InvalidTokenError, TypeError, ValueError) as exc:
            raise ValidationError("Invalid refresh token", status_code=401) from exc
        shop = db.session.get(Shop, shop_id)
        if (
            payload.get("role") != "shop"
            or TokenService.is_revoked(payload["jti"])
            or shop is None
            or not shop.is_active
        ):
            raise ValidationError("Refresh token is not authorized", status_code=401)
        TokenService.revoke(
            jti=payload["jti"],
            shop_id=shop_id,
            expires_at=datetime.fromtimestamp(payload["exp"], tz=UTC),
        )
        return ShopAuthService._token_pair(
            shop_id,
            jwt_secret=jwt_secret,
            expires_minutes=expires_minutes,
            refresh_expires_days=refresh_expires_days,
        )

    @staticmethod
    def profile(shop_id: int) -> dict:
        shop = db.session.get(Shop, shop_id)
        if shop is None or not shop.is_active:
            raise ValidationError("Shop was not found", status_code=404)
        return shop.to_dict(exclude={"password", "login_url"})
