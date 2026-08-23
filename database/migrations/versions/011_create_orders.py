"""create orders table"""
from alembic import op
import sqlalchemy as sa

revision = "011_orders"
down_revision = "010_payment_accounts"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("orders", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("shop_id", sa.BigInteger(), nullable=False), sa.Column("user_id", sa.BigInteger(), nullable=False), sa.Column("user_email", sa.String(255), nullable=False), sa.Column("order_code", sa.String(50), nullable=False), sa.Column("status", sa.String(50), nullable=False, server_default="pending"), sa.Column("order_at", sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()), sa.Column("subtotal_amount", sa.Numeric(12, 2), nullable=False), sa.Column("total_amount", sa.Numeric(12, 2), nullable=False), sa.Column("remark", sa.Text()), sa.Column("payment_account_id", sa.BigInteger(), nullable=False), sa.Column("tax_fee", sa.Numeric(12, 2), nullable=False, server_default="0.00"), sa.Column("is_pickup", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("delivery_location", sa.String(500)), sa.ForeignKeyConstraint(["shop_id"], ["shops.id"], name="fk_orders_shop_id"), sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_orders_user_id"), sa.ForeignKeyConstraint(["payment_account_id"], ["payment_accounts.id"], name="fk_orders_payment_account_id"), sa.UniqueConstraint("order_code", name="uq_orders_order_code"))
    op.create_index("ix_orders_shop_id", "orders", ["shop_id"])
    op.create_index("ix_orders_user_id", "orders", ["user_id"])
    op.create_index("ix_orders_payment_account_id", "orders", ["payment_account_id"])


def downgrade():
    op.drop_table("orders")

