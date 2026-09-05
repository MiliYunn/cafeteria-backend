from __future__ import annotations

from flask import current_app
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from extensions import db
from helpers.hash import hash_password
from helpers.shop_login import build_login_url, rebase_login_url, refresh_login_email
from models.shop import Shop
from models.category import Category
from models.shop_category import ShopCategory
from services.shared.crud_service import commit_record, delete_record, get_record, paginate_records
from services.shared.filter_service import apply_collection_filters
from validations.shared.exceptions import ValidationError


def _serialize(shop: Shop) -> dict:
    data = shop.to_dict(exclude={"password"})
    categories = db.session.execute(
        select(Category.id, Category.name)
        .join(ShopCategory, ShopCategory.category_id == Category.id)
        .where(ShopCategory.shop_id == shop.id)
        .order_by(Category.name)
    ).all()
    data["category_ids"] = [category.id for category in categories]
    data["categories"] = [{"id": category.id, "name": category.name} for category in categories]
    return data


def _sync_categories(shop_id: int, category_ids: list[int]) -> None:
    existing = (
        set(db.session.scalars(select(Category.id).where(Category.id.in_(category_ids))).all())
        if category_ids
        else set()
    )
    missing = set(category_ids) - existing
    if missing:
        raise ValidationError(
            errors={"category_ids": f"Unknown category IDs: {', '.join(map(str, sorted(missing)))}"}
        )
    db.session.execute(delete(ShopCategory).where(ShopCategory.shop_id == shop_id))
    db.session.add_all(
        ShopCategory(shop_id=shop_id, category_id=category_id) for category_id in category_ids
    )


class ShopService:
    @staticmethod
    def list(page: int, per_page: int, filters: dict) -> dict:
        statement = apply_collection_filters(
            select(Shop),
            filters,
            search_columns=(Shop.name, Shop.email, Shop.location, Shop.description),
            exact_columns={"is_active": Shop.is_active},
        ).order_by(Shop.id.desc())
        return paginate_records(statement, page, per_page, _serialize)

    @staticmethod
    def get(shop_id: int) -> dict:
        return _serialize(get_record(Shop, shop_id, "Shop"))

    @staticmethod
    def create(data: dict) -> dict:
        category_ids = data.pop("category_ids", [])
        settings = current_app.config["SETTINGS"]
        data["login_url"] = build_login_url(data["domain_url"], data["email"], data["password"], settings.shop_login_secret)
        data["password"] = hash_password(data["password"])
        shop = Shop(**data)
        db.session.add(shop)
        try:
            db.session.flush()
        except IntegrityError as exc:
            db.session.rollback()
            raise ValidationError("Shop email already exists", status_code=409) from exc
        _sync_categories(shop.id, category_ids)
        return _serialize(commit_record(shop, "Shop email already exists"))

    @staticmethod
    def update(shop_id: int, data: dict) -> dict:
        shop = get_record(Shop, shop_id, "Shop")
        category_ids = data.pop("category_ids", None)
        settings = current_app.config["SETTINGS"]
        if "password" in data:
            data["login_url"] = build_login_url(data.get("domain_url", shop.domain_url), data.get("email", shop.email), data["password"], settings.shop_login_secret)
        elif "email" in data:
            data["login_url"] = refresh_login_email(
                data.get("domain_url", shop.domain_url),
                data["email"],
                shop.login_url,
                settings.shop_login_secret,
            )
        elif "domain_url" in data:
            data["login_url"] = rebase_login_url(data["domain_url"], shop.login_url)
        if "password" in data:
            data["password"] = hash_password(data["password"])
        for field, value in data.items():
            setattr(shop, field, value)
        if category_ids is not None:
            _sync_categories(shop.id, category_ids)
        return _serialize(commit_record(shop, "Shop email already exists"))

    @staticmethod
    def delete(shop_id: int) -> None:
        delete_record(get_record(Shop, shop_id, "Shop"), "Shop has related records and cannot be deleted")
