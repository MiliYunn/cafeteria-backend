"""add timestamps to roles"""
from alembic import op
import sqlalchemy as sa
revision = "016_roles_timestamps"
down_revision = "015_revoked_tokens"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("roles", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("roles", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("roles", "updated_at")
    op.drop_column("roles", "created_at")
