"""add timestamps to shop_categories"""
from alembic import op
import sqlalchemy as sa
revision = "020_shop_categories_ts"
down_revision = "019_categories_timestamps"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("shop_categories", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("shop_categories", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("shop_categories", "updated_at")
    op.drop_column("shop_categories", "created_at")
