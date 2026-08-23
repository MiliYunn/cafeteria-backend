"""create shop_staffs table"""
from alembic import op
import sqlalchemy as sa

revision = "006_shop_staffs"
down_revision = "005_shop_categories"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("shop_staffs", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("shop_id", sa.BigInteger(), nullable=False), sa.Column("name", sa.String(255), nullable=False), sa.Column("email", sa.String(255)), sa.Column("phone", sa.String(30)), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.ForeignKeyConstraint(["shop_id"], ["shops.id"], name="fk_shop_staffs_shop_id"), sa.UniqueConstraint("email", name="uq_shop_staffs_email"))
    op.create_index("ix_shop_staffs_shop_id", "shop_staffs", ["shop_id"])


def downgrade():
    op.drop_table("shop_staffs")

