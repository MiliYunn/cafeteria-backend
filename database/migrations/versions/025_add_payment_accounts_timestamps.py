"""add timestamps to payment_accounts"""
from alembic import op
import sqlalchemy as sa
revision = "025_payment_accounts_ts"
down_revision = "024_payment_methods_ts"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("payment_accounts", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("payment_accounts", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("payment_accounts", "updated_at")
    op.drop_column("payment_accounts", "created_at")
