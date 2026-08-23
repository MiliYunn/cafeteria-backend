"""add timestamps to order_logs"""
from alembic import op
import sqlalchemy as sa
revision = "028_order_logs_ts"
down_revision = "027_order_menus_ts"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("order_logs", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("order_logs", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("order_logs", "updated_at")
    op.drop_column("order_logs", "created_at")
