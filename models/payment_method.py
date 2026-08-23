from sqlalchemy import BigInteger, Boolean, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db
from models.base import SerializableMixin


class PaymentMethod(SerializableMixin, db.Model):
    __tablename__ = "payment_methods"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    domain_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("1"))
    type: Mapped[str] = mapped_column(String(50), nullable=False)

