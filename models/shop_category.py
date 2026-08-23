from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db
from models.base import SerializableMixin


class ShopCategory(SerializableMixin, db.Model):
    __tablename__ = "shop_categories"
    __table_args__ = (UniqueConstraint("shop_id", "category_id", name="uq_shop_categories_pair"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    shop_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("shops.id"), index=True, nullable=False)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categories.id"), index=True, nullable=False)

