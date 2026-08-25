"""Public cafeteria catalog workflows."""

from sqlalchemy import select

from models.menu import Menu
from models.shop import Shop
from services.shared.crud_service import paginate_records
from services.shared.filter_service import apply_collection_filters


class CatalogService:
    @staticmethod
    def list_shops(page: int, per_page: int, filters: dict) -> dict:
        statement = apply_collection_filters(
            select(Shop).where(Shop.is_active.is_(True)),
            filters,
            search_columns=(Shop.name, Shop.location, Shop.description),
        ).order_by(Shop.name)
        return paginate_records(statement, page, per_page, lambda shop: shop.to_dict(exclude={"password"}))

    @staticmethod
    def list_shop_menus(
        shop_id: int,
        page: int,
        per_page: int,
        filters: dict,
    ) -> dict:
        statement = apply_collection_filters(
            select(Menu).where(
                Menu.shop_id == shop_id,
                Menu.is_available.is_(True),
            ),
            filters,
            search_columns=(Menu.name, Menu.description),
            exact_columns={"genre_id": Menu.genre_id},
        )
        if "min_cost" in filters:
            statement = statement.where(Menu.cost >= filters["min_cost"])
        if "max_cost" in filters:
            statement = statement.where(Menu.cost <= filters["max_cost"])
        statement = statement.order_by(Menu.name)
        return paginate_records(statement, page, per_page, lambda menu: menu.to_dict())
