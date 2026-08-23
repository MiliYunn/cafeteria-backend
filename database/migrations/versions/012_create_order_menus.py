"""create order_menus table"""
from alembic import op
import sqlalchemy as sa

revision = "012_order_menus"
down_revision = "011_orders"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("order_menus", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("order_id", sa.BigInteger(), nullable=False), sa.Column("menu_id", sa.BigInteger(), nullable=False), sa.Column("quantity", sa.BigInteger(), nullable=False), sa.Column("amount", sa.Numeric(12, 2), nullable=False), sa.ForeignKeyConstraint(["order_id"], ["orders.id"], name="fk_order_menus_order_id"), sa.ForeignKeyConstraint(["menu_id"], ["menus.id"], name="fk_order_menus_menu_id"), sa.UniqueConstraint("order_id", "menu_id", name="uq_order_menus_pair"))
    op.create_index("ix_order_menus_order_id", "order_menus", ["order_id"])
    op.create_index("ix_order_menus_menu_id", "order_menus", ["menu_id"])


def downgrade():
    op.drop_table("order_menus")

