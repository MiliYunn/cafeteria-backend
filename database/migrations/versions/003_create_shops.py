"""create shops table"""
from alembic import op
import sqlalchemy as sa

revision = "003_shops"
down_revision = "002_users"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("shops", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("name", sa.String(150), nullable=False), sa.Column("description", sa.Text()), sa.Column("logo_url", sa.String(500)), sa.Column("location", sa.String(255), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("email", sa.String(255), nullable=False), sa.Column("password", sa.String(255), nullable=False), sa.Column("open_at", sa.DateTime()), sa.Column("close_at", sa.DateTime()), sa.UniqueConstraint("email", name="uq_shops_email"))


def downgrade():
    op.drop_table("shops")

