"""Business logic for settings owned by the authenticated shop."""

from models.shop import Shop
from services.shared.crud_service import commit_record, get_record


class ShopSettingsService:
    @staticmethod
    def _shop(shop_id: int) -> Shop:
        return get_record(Shop, shop_id, "Shop")

    @staticmethod
    def _serialize(shop: Shop) -> dict:
        return {
            "shop_id": shop.id,
            "shop_name": shop.name,
            "open_at": shop.open_at.isoformat(timespec="minutes") if shop.open_at else None,
            "close_at": shop.close_at.isoformat(timespec="minutes") if shop.close_at else None,
        }

    @staticmethod
    def get(shop_id: int) -> dict:
        return ShopSettingsService._serialize(ShopSettingsService._shop(shop_id))

    @staticmethod
    def update(shop_id: int, data: dict) -> dict:
        shop = ShopSettingsService._shop(shop_id)
        for field, value in data.items():
            setattr(shop, field, value)
        return ShopSettingsService._serialize(commit_record(shop, "Shop settings could not be updated"))
