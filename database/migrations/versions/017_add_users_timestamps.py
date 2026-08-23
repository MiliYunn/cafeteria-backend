"""add timestamps to users"""
from alembic import op
import sqlalchemy as sa
revision = "017_users_timestamps"
down_revision = "016_roles_timestamps"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("users", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("users", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
