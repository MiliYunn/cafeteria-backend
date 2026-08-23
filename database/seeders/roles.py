from sqlalchemy import select

from extensions import db
from models.role import Role


def seed_roles() -> None:
    existing = set(db.session.scalars(select(Role.name)).all())
    db.session.add_all(Role(name=name) for name in ("admin", "staff", "student") if name not in existing)
    db.session.commit()

