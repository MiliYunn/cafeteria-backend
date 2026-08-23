"""create users table"""
from alembic import op
import sqlalchemy as sa

revision = "002_users"
down_revision = "001_roles"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("username", sa.String(100), nullable=False), sa.Column("email", sa.String(255), nullable=False), sa.Column("fullname", sa.String(255), nullable=False), sa.Column("role_id", sa.BigInteger(), nullable=False), sa.Column("department_id", sa.BigInteger(), nullable=True), sa.Column("password", sa.String(255), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("type", sa.String(50), nullable=False, server_default="user"), sa.ForeignKeyConstraint(["role_id"], ["roles.id"], name="fk_users_role_id"), sa.UniqueConstraint("username", name="uq_users_username"), sa.UniqueConstraint("email", name="uq_users_email"))
    op.create_index("ix_users_role_id", "users", ["role_id"])
    op.create_index("ix_users_department_id", "users", ["department_id"])


def downgrade():
    op.drop_table("users")

