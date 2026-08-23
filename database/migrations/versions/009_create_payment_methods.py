"""create payment_methods table"""
from alembic import op
import sqlalchemy as sa

revision = "009_payment_methods"
down_revision = "008_menus"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("payment_methods", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("name", sa.String(100), nullable=False), sa.Column("description", sa.Text()), sa.Column("logo", sa.String(500)), sa.Column("domain_url", sa.String(500)), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("type", sa.String(50), nullable=False), sa.UniqueConstraint("name", name="uq_payment_methods_name"))


def downgrade():
    op.drop_table("payment_methods")

