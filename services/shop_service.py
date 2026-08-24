from __future__ import annotations

from sqlalchemy import select

from extensions import db
from helpers.hash import hash_password
from models.shop import Shop
from services.crud_service import commit_record, delete_record, get_record, paginate_records


def _serialize(shop: Shop) -> dict:
    return shop.to_dict(exclude={"password"})


class ShopService:
    @staticmethod
    def list(page: int, per_page: int) -> dict:
        return paginate_records(select(Shop).order_by(Shop.id.desc()), page, per_page, _serialize)

    @staticmethod
    def get(shop_id: int) -> dict:
        return _serialize(get_record(Shop, shop_id, "Shop"))

    @staticmethod
    def create(data: dict) -> dict:
        data["password"] = hash_password(data["password"])
        shop = Shop(**data)
        db.session.add(shop)
        return _serialize(commit_record(shop, "Shop email already exists"))

    @staticmethod
    def update(shop_id: int, data: dict) -> dict:
        shop = get_record(Shop, shop_id, "Shop")
        if "password" in data:
            data["password"] = hash_password(data["password"])
        for field, value in data.items():
            setattr(shop, field, value)
        return _serialize(commit_record(shop, "Shop email already exists"))

    @staticmethod
    def delete(shop_id: int) -> None:
        delete_record(get_record(Shop, shop_id, "Shop"), "Shop has related records and cannot be deleted")
