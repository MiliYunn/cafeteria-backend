"""Add a role to each shop staff member."""

from alembic import op
import sqlalchemy as sa


revision = "036_add_shop_staff_role"
down_revision = "035_create_menu_genres"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "shop_staffs",
        sa.Column("role", sa.String(length=50), server_default="staff", nullable=False),
    )


def downgrade():
    op.drop_column("shop_staffs", "role")
