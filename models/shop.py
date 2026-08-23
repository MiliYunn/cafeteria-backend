from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db
from models.base import SerializableMixin


class Shop(SerializableMixin, db.Model):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("1"))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    open_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    close_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

