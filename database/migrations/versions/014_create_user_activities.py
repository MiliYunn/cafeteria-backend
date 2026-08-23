"""create user_activities table"""
from alembic import op
import sqlalchemy as sa

revision = "014_user_activities"
down_revision = "013_order_logs"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("user_activities", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("user_id", sa.BigInteger(), nullable=False), sa.Column("activity", sa.Text(), nullable=False), sa.Column("active_at", sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()), sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_user_activities_user_id"))
    op.create_index("ix_user_activities_user_id", "user_activities", ["user_id"])


def downgrade():
    op.drop_table("user_activities")

