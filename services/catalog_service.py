"""Public cafeteria catalog workflows."""

from sqlalchemy import select

from models.menu import Menu
from models.shop import Shop
from services.crud_service import paginate_records


class CatalogService:
    @staticmethod
    def list_shops(page: int, per_page: int) -> dict:
        statement = select(Shop).where(Shop.is_active.is_(True)).order_by(Shop.name)
        return paginate_records(statement, page, per_page, lambda shop: shop.to_dict(exclude={"password"}))

    @staticmethod
    def list_shop_menus(shop_id: int, page: int, per_page: int) -> dict:
        statement = (
            select(Menu)
            .where(Menu.shop_id == shop_id, Menu.is_available.is_(True))
            .order_by(Menu.name)
        )
        return paginate_records(statement, page, per_page, lambda menu: menu.to_dict())
