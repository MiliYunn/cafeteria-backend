from datetime import datetime

from sqlalchemy import TIMESTAMP, BigInteger, ForeignKey, UniqueConstraint, func, text
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db
from models.base import SerializableMixin


class MenuGenre(SerializableMixin, db.Model):
    __tablename__ = "menu_genres"
    __table_args__ = (UniqueConstraint("menu_id", "genre_id", name="uq_menu_genres_pair"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    menu_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("menus.id"), index=True, nullable=False)
    genre_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("genres.id"), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), onupdate=func.current_timestamp())
