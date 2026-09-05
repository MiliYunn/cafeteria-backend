"""Allow revoked JWTs to belong to a user or a shop."""

from alembic import op
import sqlalchemy as sa

revision = "034_add_shop_token_revocation"
down_revision = "033_add_shop_urls"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "revoked_tokens",
        "user_id",
        existing_type=sa.BigInteger(),
        nullable=True,
    )
    op.add_column("revoked_tokens", sa.Column("shop_id", sa.BigInteger(), nullable=True))
    op.create_index("ix_revoked_tokens_shop_id", "revoked_tokens", ["shop_id"])
    op.create_foreign_key(
        "fk_revoked_tokens_shop_id",
        "revoked_tokens",
        "shops",
        ["shop_id"],
        ["id"],
    )


def downgrade():
    op.execute("DELETE FROM revoked_tokens WHERE user_id IS NULL")
    op.drop_constraint("fk_revoked_tokens_shop_id", "revoked_tokens", type_="foreignkey")
    op.drop_index("ix_revoked_tokens_shop_id", table_name="revoked_tokens")
    op.drop_column("revoked_tokens", "shop_id")
    op.alter_column(
        "revoked_tokens",
        "user_id",
        existing_type=sa.BigInteger(),
        nullable=False,
    )
