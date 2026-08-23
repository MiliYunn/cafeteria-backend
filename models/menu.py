from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, ForeignKey, Numeric, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db
from models.base import SerializableMixin


class Menu(SerializableMixin, db.Model):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    shop_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("shops.id"), index=True, nullable=False)
    genre_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("genres.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("1"))
    image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

