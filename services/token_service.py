"""JWT revocation workflows."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from extensions import db
from models.revoked_token import RevokedToken


class TokenService:
    @staticmethod
    def is_revoked(jti: str) -> bool:
        return db.session.scalar(
            select(RevokedToken.id).where(RevokedToken.jti == jti)
        ) is not None

    @staticmethod
    def revoke(*, jti: str, user_id: int, expires_at: datetime) -> None:
        if TokenService.is_revoked(jti):
            return
        db.session.add(
            RevokedToken(
                jti=jti,
                user_id=user_id,
                expires_at=expires_at.astimezone(UTC).replace(tzinfo=None),
            )
        )
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

