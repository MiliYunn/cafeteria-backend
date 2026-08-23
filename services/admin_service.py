"""Administrative business workflows."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from extensions import db
from models.category import Category
from models.user import User
from validations.exceptions import ValidationError


class AdminService:
    @staticmethod
    def list_users() -> list[dict]:
        users = db.session.scalars(select(User).order_by(User.id.desc())).all()
        return [user.to_dict(exclude={"password"}) for user in users]

    @staticmethod
    def list_categories() -> list[dict]:
        categories = db.session.scalars(select(Category).order_by(Category.name)).all()
        return [category.to_dict() for category in categories]

    @staticmethod
    def create_category(data: dict) -> dict:
        category = Category(**data)
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError as exc:
            db.session.rollback()
            raise ValidationError("Category already exists", {"name": "Name must be unique"}, 409) from exc
        return category.to_dict()

