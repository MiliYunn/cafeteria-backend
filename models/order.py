from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Numeric, String, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db
from models.base import SerializableMixin


class Order(SerializableMixin, db.Model):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    shop_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("shops.id"), index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True, nullable=False)
    user_email: Mapped[str] = mapped_column(String(255), nullable=False)
    order_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, server_default="pending")
    order_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    subtotal_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    payment_account_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("payment_accounts.id"), index=True, nullable=False)
    tax_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, server_default="0.00")
    is_pickup: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("1"))
    delivery_location: Mapped[str | None] = mapped_column(String(500), nullable=True)

