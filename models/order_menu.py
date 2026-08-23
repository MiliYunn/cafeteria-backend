from decimal import Decimal

from sqlalchemy import BigInteger, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db
from models.base import SerializableMixin


class OrderMenu(SerializableMixin, db.Model):
    __tablename__ = "order_menus"
    __table_args__ = (UniqueConstraint("order_id", "menu_id", name="uq_order_menus_pair"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("orders.id"), index=True, nullable=False)
    menu_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("menus.id"), index=True, nullable=False)
    quantity: Mapped[int] = mapped_column(BigInteger, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

