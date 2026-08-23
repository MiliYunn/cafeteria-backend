"""add timestamps to genres"""
from alembic import op
import sqlalchemy as sa
revision = "022_genres_timestamps"
down_revision = "021_shop_staffs_ts"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("genres", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("genres", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("genres", "updated_at")
    op.drop_column("genres", "created_at")
