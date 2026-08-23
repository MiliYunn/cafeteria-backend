"""add shop_id to payment_accounts"""
from alembic import op
import sqlalchemy as sa

revision = "031_payment_accounts_shop"
down_revision = "030_revoked_tokens_ts"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "payment_accounts",
        sa.Column("shop_id", sa.BigInteger(), nullable=False),
    )
    op.create_index(
        "ix_payment_accounts_shop_id",
        "payment_accounts",
        ["shop_id"],
    )
    op.create_foreign_key(
        "fk_payment_accounts_shop_id",
        "payment_accounts",
        "shops",
        ["shop_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint(
        "fk_payment_accounts_shop_id",
        "payment_accounts",
        type_="foreignkey",
    )
    op.drop_index("ix_payment_accounts_shop_id", table_name="payment_accounts")
    op.drop_column("payment_accounts", "shop_id")

