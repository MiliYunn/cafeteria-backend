"""add timestamps to orders"""
from alembic import op
import sqlalchemy as sa
revision = "026_orders_timestamps"
down_revision = "025_payment_accounts_ts"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("orders", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("orders", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("orders", "updated_at")
    op.drop_column("orders", "created_at")
