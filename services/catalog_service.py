"""Public cafeteria catalog workflows."""

from sqlalchemy import select

from extensions import db
from models.menu import Menu
from models.shop import Shop


class CatalogService:
    @staticmethod
    def list_shops() -> list[dict]:
        shops = db.session.scalars(select(Shop).where(Shop.is_active.is_(True)).order_by(Shop.name)).all()
        return [shop.to_dict(exclude={"password"}) for shop in shops]

    @staticmethod
    def list_shop_menus(shop_id: int) -> list[dict]:
        menus = db.session.scalars(
            select(Menu)
            .where(Menu.shop_id == shop_id, Menu.is_available.is_(True))
            .order_by(Menu.name)
        ).all()
        return [menu.to_dict() for menu in menus]

