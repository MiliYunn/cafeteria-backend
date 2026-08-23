from sqlalchemy import BigInteger, Boolean, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db
from models.base import SerializableMixin


class ShopStaff(SerializableMixin, db.Model):
    __tablename__ = "shop_staffs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    shop_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("shops.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("1"))

