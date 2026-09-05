"""Environment-backed application configuration."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


def _json_list(name: str, default: list[str]) -> list[str]:
    raw = os.getenv(name)
    if not raw:
        return default
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{name} must be a JSON array") from exc
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{name} must be a JSON array of strings")
    return value


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str
    app_env: str
    app_port: int
    allow_origins: list[str]
    trusted_hosts: list[str]
    jwt_secret: str
    jwt_expires_minutes: int
    jwt_refresh_expires_days: int
    shop_login_secret: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    rate_admin_per_min: int
    rate_api_per_min: int
    storage: str
    local_storage_path: str
    max_upload_mb: int
    allowed_upload_extensions: list[str]
    log_level: str

    @property
    def database_uri(self) -> str:
        user = quote_plus(self.db_user)
        password = quote_plus(self.db_password)
        return (
            f"mysql+pymysql://{user}:{password}@{self.db_host}:{self.db_port}/"
            f"{self.db_name}?charset=utf8mb4"
        )

    @classmethod
    def from_env(cls) -> "Settings":
        settings = cls(
            app_name=os.getenv("APP_NAME", "APCafeteria"),
            app_env=os.getenv("APP_ENV", "dev"),
            app_port=int(os.getenv("APP_PORT", "8000")),
            allow_origins=_json_list("ALLOW_ORIGINS", ["http://localhost:5173"]),
            trusted_hosts=_json_list("TRUSTED_HOSTS", ["127.0.0.1", "localhost"]),
            jwt_secret=os.getenv("JWT_SECRET", ""),
            jwt_expires_minutes=int(os.getenv("JWT_EXPIRES_MINUTES", "60")),
            jwt_refresh_expires_days=int(os.getenv("JWT_REFRESH_EXPIRES_DAYS", "7")),
            shop_login_secret=os.getenv("SHOP_LOGIN_SECRET", ""),
            db_host=os.getenv("DB_HOST", "127.0.0.1"),
            db_port=int(os.getenv("DB_PORT", "3306")),
            db_name=os.getenv("DB_NAME", "cafeteria"),
            db_user=os.getenv("DB_USER", "root"),
            db_password=os.getenv("DB_PASSWORD", "secret"),
            rate_admin_per_min=int(os.getenv("RATE_ADMIN_PER_MIN", "30")),
            rate_api_per_min=int(os.getenv("RATE_API_PER_MIN", "60")),
            storage=os.getenv("STORAGE", "local").lower(),
            local_storage_path=os.getenv("LOCAL_STORAGE_PATH", "uploads"),
            max_upload_mb=int(os.getenv("MAX_UPLOAD_MB", "5")),
            allowed_upload_extensions=_json_list(
                "ALLOWED_UPLOAD_EXTENSIONS",
                ["jpg", "jpeg", "png", "webp", "gif", "pdf"],
            ),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
        if len(settings.jwt_secret) < 32:
            raise ValueError("JWT_SECRET must contain at least 32 characters")
        if settings.jwt_expires_minutes < 1:
            raise ValueError("JWT_EXPIRES_MINUTES must be at least 1")
        if settings.jwt_refresh_expires_days < 1:
            raise ValueError("JWT_REFRESH_EXPIRES_DAYS must be at least 1")
        if len(settings.shop_login_secret) < 32:
            raise ValueError("SHOP_LOGIN_SECRET must contain at least 32 characters")
        if settings.storage != "local":
            raise ValueError("Only STORAGE=local is currently supported")
        storage_path = Path(settings.local_storage_path)
        if storage_path.is_absolute() or ".." in storage_path.parts:
            raise ValueError("LOCAL_STORAGE_PATH must stay inside the project")
        if settings.max_upload_mb < 1:
            raise ValueError("MAX_UPLOAD_MB must be at least 1")
        return settings


class FlaskConfig:
    def __init__(self, settings: Settings):
        self.SQLALCHEMY_DATABASE_URI = settings.database_uri
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 1800,
        }
        self.TRUSTED_HOSTS = settings.trusted_hosts
        self.JSON_SORT_KEYS = False
        self.STORAGE = settings.storage
        self.UPLOAD_FOLDER = str(
            (Path(__file__).resolve().parent / settings.local_storage_path).resolve()
        )
        self.MAX_CONTENT_LENGTH = settings.max_upload_mb * 1024 * 1024
        self.ALLOWED_UPLOAD_EXTENSIONS = {
            extension.lower().lstrip(".")
            for extension in settings.allowed_upload_extensions
        }
