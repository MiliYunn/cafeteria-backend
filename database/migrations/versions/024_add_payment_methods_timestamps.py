"""add timestamps to payment_methods"""
from alembic import op
import sqlalchemy as sa
revision = "024_payment_methods_ts"
down_revision = "023_menus_timestamps"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("payment_methods", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("payment_methods", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("payment_methods", "updated_at")
    op.drop_column("payment_methods", "created_at")
