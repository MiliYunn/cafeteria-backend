"""create shop_categories table"""
from alembic import op
import sqlalchemy as sa

revision = "005_shop_categories"
down_revision = "004_categories"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("shop_categories", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("shop_id", sa.BigInteger(), nullable=False), sa.Column("category_id", sa.BigInteger(), nullable=False), sa.ForeignKeyConstraint(["shop_id"], ["shops.id"], name="fk_shop_categories_shop_id"), sa.ForeignKeyConstraint(["category_id"], ["categories.id"], name="fk_shop_categories_category_id"), sa.UniqueConstraint("shop_id", "category_id", name="uq_shop_categories_pair"))
    op.create_index("ix_shop_categories_shop_id", "shop_categories", ["shop_id"])
    op.create_index("ix_shop_categories_category_id", "shop_categories", ["category_id"])


def downgrade():
    op.drop_table("shop_categories")

