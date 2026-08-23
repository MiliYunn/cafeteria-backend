import os

from sqlalchemy import or_, select

from extensions import db
from helpers.hash import hash_password
from models.role import Role
from models.user import User


def seed_admin_user() -> None:
    username = "admin"
    email = "admin@example.com"
    password = "admin123"
    if len(password) < 6 or password == "change-me-before-use":
        raise ValueError("Set SEED_ADMIN_PASSWORD to a non-default value of at least 6 characters")
    if db.session.scalar(select(User).where(or_(User.username == username, User.email == email))):
        return
    role = db.session.scalar(select(Role).where(Role.name == "admin", Role.is_active.is_(True)))
    if role is None:
        raise RuntimeError("Admin role is missing; run the role seeder first")
    db.session.add(User(username=username, email=email, fullname="System Administrator", role_id=role.id, password=hash_password(password), type="admin"))
    db.session.commit()

