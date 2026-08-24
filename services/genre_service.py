from __future__ import annotations

from sqlalchemy import select

from extensions import db
from models.genre import Genre
from services.crud_service import commit_record, delete_record, get_record, paginate_records


class GenreService:
    @staticmethod
    def list(page: int, per_page: int) -> dict:
        return paginate_records(select(Genre).order_by(Genre.id.desc()), page, per_page, lambda item: item.to_dict())

    @staticmethod
    def options() -> list[dict]:
        items = db.session.scalars(select(Genre).where(Genre.is_active.is_(True)).order_by(Genre.name)).all()
        return [{"id": item.id, "name": item.name} for item in items]

    @staticmethod
    def get(genre_id: int) -> dict:
        return get_record(Genre, genre_id, "Genre").to_dict()

    @staticmethod
    def create(data: dict) -> dict:
        item = Genre(**data)
        db.session.add(item)
        return commit_record(item, "Genre name already exists").to_dict()

    @staticmethod
    def update(genre_id: int, data: dict) -> dict:
        item = get_record(Genre, genre_id, "Genre")
        for field, value in data.items():
            setattr(item, field, value)
        return commit_record(item, "Genre name already exists").to_dict()

    @staticmethod
    def delete(genre_id: int) -> None:
        delete_record(get_record(Genre, genre_id, "Genre"), "Genre is being used and cannot be deleted")
