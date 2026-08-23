"""add timestamps to shop_staffs"""
from alembic import op
import sqlalchemy as sa
revision = "021_shop_staffs_ts"
down_revision = "020_shop_categories_ts"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("shop_staffs", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("shop_staffs", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("shop_staffs", "updated_at")
    op.drop_column("shop_staffs", "created_at")
