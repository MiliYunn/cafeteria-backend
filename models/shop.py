from datetime import datetime, time

from sqlalchemy import TIMESTAMP, BigInteger, Boolean, Time, String, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db
from models.base import SerializableMixin


class Shop(SerializableMixin, db.Model):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    domain_url: Mapped[str] = mapped_column(String(500), nullable=False)
    login_url: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("1"))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    open_at: Mapped[time | None] = mapped_column(Time, nullable=True)
    close_at: Mapped[time | None] = mapped_column(Time, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), onupdate=func.current_timestamp())
