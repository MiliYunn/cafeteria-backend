"""Add shop portal domain and generated login URLs."""

from alembic import op
import sqlalchemy as sa

revision = "033_add_shop_urls"
down_revision = "032_shops_time_only"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("shops", sa.Column("domain_url", sa.String(500), nullable=True))
    op.add_column("shops", sa.Column("login_url", sa.Text(), nullable=True))
    op.execute("UPDATE shops SET domain_url = 'http://localhost:5174', login_url = ''")
    op.alter_column("shops", "domain_url", existing_type=sa.String(500), nullable=False)
    op.alter_column("shops", "login_url", existing_type=sa.Text(), nullable=False)


def downgrade():
    op.drop_column("shops", "login_url")
    op.drop_column("shops", "domain_url")
