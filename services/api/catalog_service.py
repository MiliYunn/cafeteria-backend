"""Public cafeteria catalog workflows."""

from sqlalchemy import select

from extensions import db
from models.category import Category
from models.menu import Menu
from models.menu_genre import MenuGenre
from models.shop_category import ShopCategory
from services.shop.menu_service import MenuService
from models.shop import Shop
from services.shared.crud_service import paginate_records
from services.shared.filter_service import apply_collection_filters


class CatalogService:
    @staticmethod
    def _serialize_shop(shop: Shop) -> dict:
        data = shop.to_dict(exclude={"password", "email", "login_url"})
        categories = db.session.execute(
            select(Category.id, Category.name)
            .join(ShopCategory, ShopCategory.category_id == Category.id)
            .where(ShopCategory.shop_id == shop.id, Category.is_active.is_(True))
            .order_by(Category.name)
        ).all()
        data["categories"] = [
            {"id": category.id, "name": category.name} for category in categories
        ]
        return data

    @staticmethod
    def list_shops(page: int, per_page: int, filters: dict) -> dict:
        statement = apply_collection_filters(
            select(Shop).where(Shop.is_active.is_(True)),
            filters,
            search_columns=(Shop.name, Shop.location, Shop.description),
        ).order_by(Shop.name)
        return paginate_records(statement, page, per_page, CatalogService._serialize_shop)

    @staticmethod
    def list_shop_menus(
        shop_id: int,
        page: int,
        per_page: int,
        filters: dict,
    ) -> dict:
        shop = db.session.get(Shop, shop_id)
        if shop is None or not shop.is_active:
            from validations.shared.exceptions import ValidationError

            raise ValidationError("Shop not found", status_code=404)
        genre_id = filters.pop("genre_id", None)
        statement = apply_collection_filters(
            select(Menu).where(
                Menu.shop_id == shop_id,
                Menu.is_available.is_(True),
            ),
            filters,
            search_columns=(Menu.name, Menu.description),
        )
        if genre_id is not None:
            statement = statement.join(MenuGenre, MenuGenre.menu_id == Menu.id).where(MenuGenre.genre_id == genre_id)
        if "min_cost" in filters:
            statement = statement.where(Menu.cost >= filters["min_cost"])
        if "max_cost" in filters:
            statement = statement.where(Menu.cost <= filters["max_cost"])
        statement = statement.order_by(Menu.name)
        return paginate_records(statement, page, per_page, MenuService._serialize)
