"""create roles table"""
from alembic import op
import sqlalchemy as sa

revision = "001_roles"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("roles", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("name", sa.String(50), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.UniqueConstraint("name", name="uq_roles_name"))


def downgrade():
    op.drop_table("roles")

