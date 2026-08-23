"""create categories table"""
from alembic import op
import sqlalchemy as sa

revision = "004_categories"
down_revision = "003_shops"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("categories", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("name", sa.String(100), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("description", sa.Text()), sa.UniqueConstraint("name", name="uq_categories_name"))


def downgrade():
    op.drop_table("categories")

