from __future__ import annotations

from sqlalchemy import select

from extensions import db
from models.shop import Shop
from models.shop_staff import ShopStaff
from services.shared.crud_service import commit_record, delete_record, get_record, paginate_records
from services.shared.filter_service import apply_collection_filters
from validations.shared.exceptions import ValidationError


class ShopStaffService:
    @staticmethod
    def _shop(shop_id: int) -> None:
        get_record(Shop, shop_id, "Shop")

    @staticmethod
    def _staff(shop_id: int, staff_id: int) -> ShopStaff:
        staff = get_record(ShopStaff, staff_id, "Shop staff")
        if staff.shop_id != shop_id:
            raise ValidationError("Shop staff not found", status_code=404)
        return staff

    @staticmethod
    def list(shop_id: int, page: int, per_page: int, filters: dict) -> dict:
        ShopStaffService._shop(shop_id)
        statement = apply_collection_filters(
            select(ShopStaff).where(ShopStaff.shop_id == shop_id),
            filters,
            search_columns=(ShopStaff.name, ShopStaff.email, ShopStaff.phone),
            exact_columns={"is_active": ShopStaff.is_active, "role": ShopStaff.role},
        ).order_by(ShopStaff.id.desc())
        return paginate_records(statement, page, per_page, lambda item: item.to_dict())

    @staticmethod
    def get(shop_id: int, staff_id: int) -> dict:
        return ShopStaffService._staff(shop_id, staff_id).to_dict()

    @staticmethod
    def create(shop_id: int, data: dict) -> dict:
        ShopStaffService._shop(shop_id)
        staff = ShopStaff(shop_id=shop_id, **data)
        db.session.add(staff)
        return commit_record(staff, "Shop staff email already exists").to_dict()

    @staticmethod
    def update(shop_id: int, staff_id: int, data: dict) -> dict:
        staff = ShopStaffService._staff(shop_id, staff_id)
        for field, value in data.items():
            setattr(staff, field, value)
        return commit_record(staff, "Shop staff email already exists").to_dict()

    @staticmethod
    def delete(shop_id: int, staff_id: int) -> None:
        delete_record(ShopStaffService._staff(shop_id, staff_id), "Shop staff cannot be deleted")
