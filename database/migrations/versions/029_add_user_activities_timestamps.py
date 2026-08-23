"""add timestamps to user_activities"""
from alembic import op
import sqlalchemy as sa
revision = "029_user_activities_ts"
down_revision = "028_order_logs_ts"
branch_labels = None
depends_on = None
def upgrade():
    op.add_column("user_activities", sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))
    op.add_column("user_activities", sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")))
def downgrade():
    op.drop_column("user_activities", "updated_at")
    op.drop_column("user_activities", "created_at")
