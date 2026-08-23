"""create order_logs table"""
from alembic import op
import sqlalchemy as sa

revision = "013_order_logs"
down_revision = "012_order_menus"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("order_logs", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("order_id", sa.BigInteger(), nullable=False), sa.Column("status", sa.String(50), nullable=False), sa.Column("user_id", sa.BigInteger()), sa.ForeignKeyConstraint(["order_id"], ["orders.id"], name="fk_order_logs_order_id"), sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_order_logs_user_id"))
    op.create_index("ix_order_logs_order_id", "order_logs", ["order_id"])
    op.create_index("ix_order_logs_user_id", "order_logs", ["user_id"])


def downgrade():
    op.drop_table("order_logs")

