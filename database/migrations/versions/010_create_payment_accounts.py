"""create payment_accounts table"""
from alembic import op
import sqlalchemy as sa

revision = "010_payment_accounts"
down_revision = "009_payment_methods"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("payment_accounts", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("payment_method_id", sa.BigInteger(), nullable=False), sa.Column("account_holder_name", sa.String(255), nullable=False), sa.Column("account_number", sa.String(100), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("image", sa.String(500)), sa.ForeignKeyConstraint(["payment_method_id"], ["payment_methods.id"], name="fk_payment_accounts_payment_method_id"))
    op.create_index("ix_payment_accounts_payment_method_id", "payment_accounts", ["payment_method_id"])


def downgrade():
    op.drop_table("payment_accounts")

