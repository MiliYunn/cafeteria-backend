"""Shop portal endpoint registration."""

from flask import Blueprint

shop_bp = Blueprint("shop", __name__, url_prefix="/shop")

