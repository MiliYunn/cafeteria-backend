"""Import every model so SQLAlchemy and Alembic share complete metadata."""

from models.category import Category
from models.genre import Genre
from models.menu import Menu
from models.menu_genre import MenuGenre
from models.order import Order
from models.order_log import OrderLog
from models.order_menu import OrderMenu
from models.payment_account import PaymentAccount
from models.payment_method import PaymentMethod
from models.role import Role
from models.revoked_token import RevokedToken
from models.shop import Shop
from models.shop_category import ShopCategory
from models.shop_staff import ShopStaff
from models.user import User
from models.user_activity import UserActivity

__all__ = [
    "Category", "Genre", "Menu", "MenuGenre", "Order", "OrderLog", "OrderMenu",
    "PaymentAccount", "PaymentMethod", "Role", "RevokedToken", "Shop", "ShopCategory",
    "ShopStaff", "User", "UserActivity",
]
