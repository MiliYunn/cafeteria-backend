"""add timestamps to revoked_tokens"""
from alembic import op
import sqlalchemy as sa
revision = "030_revoked_tokens_ts"
down_revision = "029_user_activities_ts"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("revoked_tokens", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("revoked_tokens", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("revoked_tokens", "updated_at")
    op.drop_column("revoked_tokens", "created_at")
