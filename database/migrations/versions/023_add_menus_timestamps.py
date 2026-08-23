"""add timestamps to menus"""
from alembic import op
import sqlalchemy as sa
revision = "023_menus_timestamps"
down_revision = "022_genres_timestamps"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("menus", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("menus", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("menus", "updated_at")
    op.drop_column("menus", "created_at")
