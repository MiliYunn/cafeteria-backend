"""create genres table"""
from alembic import op
import sqlalchemy as sa

revision = "007_genres"
down_revision = "006_shop_staffs"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("genres", sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True), sa.Column("name", sa.String(100), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.UniqueConstraint("name", name="uq_genres_name"))


def downgrade():
    op.drop_table("genres")

