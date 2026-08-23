from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db
from models.base import SerializableMixin


class UserActivity(SerializableMixin, db.Model):
    __tablename__ = "user_activities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), index=True, nullable=False)
    activity: Mapped[str] = mapped_column(Text, nullable=False)
    active_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())

