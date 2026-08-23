"""add timestamps to shops"""
from alembic import op
import sqlalchemy as sa
revision = "018_shops_timestamps"
down_revision = "017_users_timestamps"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("shops", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("shops", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("shops", "updated_at")
    op.drop_column("shops", "created_at")
