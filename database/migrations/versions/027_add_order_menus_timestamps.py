"""add timestamps to order_menus"""
from alembic import op
import sqlalchemy as sa
revision = "027_order_menus_ts"
down_revision = "026_orders_timestamps"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("order_menus", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("order_menus", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("order_menus", "updated_at")
    op.drop_column("order_menus", "created_at")
