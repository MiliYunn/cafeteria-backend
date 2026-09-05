"""Business logic for shop-owned menu items."""

from sqlalchemy import delete, select

from extensions import db
from models.genre import Genre
from models.menu import Menu
from models.menu_genre import MenuGenre
from models.shop import Shop
from services.shared.crud_service import commit_record, delete_record, get_record, paginate_records
from services.shared.filter_service import apply_collection_filters
from validations.shared.exceptions import ValidationError


class MenuService:
    @staticmethod
    def _shop(shop_id: int) -> None:
        get_record(Shop, shop_id, "Shop")

    @staticmethod
    def _menu(shop_id: int, menu_id: int) -> Menu:
        menu = get_record(Menu, menu_id, "Menu item")
        if menu.shop_id != shop_id:
            raise ValidationError("Menu item not found", status_code=404)
        return menu

    @staticmethod
    def _serialize(menu: Menu) -> dict:
        data = menu.to_dict()
        genres = db.session.execute(
            select(Genre.id, Genre.name)
            .join(MenuGenre, MenuGenre.genre_id == Genre.id)
            .where(MenuGenre.menu_id == menu.id)
            .order_by(Genre.name)
        ).all()
        data["genre_ids"] = [genre.id for genre in genres]
        data["genres"] = [{"id": genre.id, "name": genre.name} for genre in genres]
        return data

    @staticmethod
    def _sync_genres(menu_id: int, genre_ids: list[int]) -> None:
        existing = set(db.session.scalars(select(Genre.id).where(Genre.id.in_(genre_ids))).all())
        missing = set(genre_ids) - existing
        if missing:
            raise ValidationError(errors={"genre_ids": f"Unknown genre IDs: {', '.join(map(str, sorted(missing)))}"})
        db.session.execute(delete(MenuGenre).where(MenuGenre.menu_id == menu_id))
        db.session.add_all(MenuGenre(menu_id=menu_id, genre_id=genre_id) for genre_id in genre_ids)

    @staticmethod
    def list(shop_id: int, page: int, per_page: int, filters: dict) -> dict:
        MenuService._shop(shop_id)
        genre_id = filters.pop("genre_id", None)
        statement = apply_collection_filters(
            select(Menu).where(Menu.shop_id == shop_id),
            filters,
            search_columns=(Menu.name, Menu.description),
            exact_columns={"is_available": Menu.is_available},
        ).order_by(Menu.id.desc())
        if genre_id is not None:
            statement = statement.join(MenuGenre, MenuGenre.menu_id == Menu.id).where(MenuGenre.genre_id == genre_id)
        return paginate_records(statement, page, per_page, MenuService._serialize)

    @staticmethod
    def get(shop_id: int, menu_id: int) -> dict:
        return MenuService._serialize(MenuService._menu(shop_id, menu_id))

    @staticmethod
    def create(shop_id: int, data: dict) -> dict:
        MenuService._shop(shop_id)
        genre_ids = data.pop("genre_ids")
        menu = Menu(shop_id=shop_id, **data)
        db.session.add(menu)
        db.session.flush()
        MenuService._sync_genres(menu.id, genre_ids)
        return MenuService._serialize(commit_record(menu, "Menu item could not be created"))

    @staticmethod
    def update(shop_id: int, menu_id: int, data: dict) -> dict:
        menu = MenuService._menu(shop_id, menu_id)
        genre_ids = data.pop("genre_ids", None)
        for field, value in data.items():
            setattr(menu, field, value)
        if genre_ids is not None:
            MenuService._sync_genres(menu.id, genre_ids)
        return MenuService._serialize(commit_record(menu, "Menu item could not be updated"))

    @staticmethod
    def delete(shop_id: int, menu_id: int) -> None:
        delete_record(MenuService._menu(shop_id, menu_id), "Menu item is being used and cannot be deleted")
