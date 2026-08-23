from sqlalchemy import BigInteger, Boolean, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db
from models.base import SerializableMixin


class PaymentAccount(SerializableMixin, db.Model):
    __tablename__ = "payment_accounts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    payment_method_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("payment_methods.id"), index=True, nullable=False)
    account_holder_name: Mapped[str] = mapped_column(String(255), nullable=False)
    account_number: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("1"))
    image: Mapped[str | None] = mapped_column(String(500), nullable=True)

