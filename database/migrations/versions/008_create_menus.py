"""create menus table"""
from alembic import op
import sqlalchemy as sa

revision = "008_menus"
down_revision = "007_genres"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("menus", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("shop_id", sa.BigInteger(), nullable=False), sa.Column("genre_id", sa.BigInteger(), nullable=False), sa.Column("name", sa.String(150), nullable=False), sa.Column("cost", sa.Numeric(12, 2), nullable=False), sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("image", sa.String(500)), sa.Column("description", sa.Text()), sa.ForeignKeyConstraint(["shop_id"], ["shops.id"], name="fk_menus_shop_id"), sa.ForeignKeyConstraint(["genre_id"], ["genres.id"], name="fk_menus_genre_id"))
    op.create_index("ix_menus_shop_id", "menus", ["shop_id"])
    op.create_index("ix_menus_genre_id", "menus", ["genre_id"])


def downgrade():
    op.drop_table("menus")

