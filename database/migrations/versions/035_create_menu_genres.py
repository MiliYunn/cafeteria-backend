"""Allow each menu item to belong to multiple genres."""

from alembic import op
import sqlalchemy as sa


revision = "035_create_menu_genres"
down_revision = "034_add_shop_token_revocation"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "menu_genres",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("menu_id", sa.BigInteger(), nullable=False),
        sa.Column("genre_id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["genre_id"], ["genres.id"], name="fk_menu_genres_genre_id"),
        sa.ForeignKeyConstraint(["menu_id"], ["menus.id"], name="fk_menu_genres_menu_id"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("menu_id", "genre_id", name="uq_menu_genres_pair"),
    )
    op.create_index("ix_menu_genres_menu_id", "menu_genres", ["menu_id"])
    op.create_index("ix_menu_genres_genre_id", "menu_genres", ["genre_id"])
    op.execute("INSERT INTO menu_genres (menu_id, genre_id) SELECT id, genre_id FROM menus")
    op.drop_constraint("fk_menus_genre_id", "menus", type_="foreignkey")
    op.drop_index("ix_menus_genre_id", table_name="menus")
    op.drop_column("menus", "genre_id")


def downgrade():
    op.add_column("menus", sa.Column("genre_id", sa.BigInteger(), nullable=True))
    op.execute("UPDATE menus SET genre_id = (SELECT MIN(mg.genre_id) FROM menu_genres mg WHERE mg.menu_id = menus.id)")
    op.alter_column("menus", "genre_id", existing_type=sa.BigInteger(), nullable=False)
    op.create_index("ix_menus_genre_id", "menus", ["genre_id"])
    op.create_foreign_key("fk_menus_genre_id", "menus", "genres", ["genre_id"], ["id"])
    op.drop_index("ix_menu_genres_genre_id", table_name="menu_genres")
    op.drop_index("ix_menu_genres_menu_id", table_name="menu_genres")
    op.drop_table("menu_genres")
