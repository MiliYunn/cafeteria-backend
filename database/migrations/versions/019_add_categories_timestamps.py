"""add timestamps to categories"""
from alembic import op
import sqlalchemy as sa
revision = "019_categories_timestamps"
down_revision = "018_shops_timestamps"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("categories", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("categories", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("categories", "updated_at")
    op.drop_column("categories", "created_at")
