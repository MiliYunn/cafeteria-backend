"""Add the delivery-dependent service fee to orders."""

from alembic import op
import sqlalchemy as sa


revision = "037_add_orders_service_fee"
down_revision = "036_add_shop_staff_role"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "orders",
        sa.Column(
            "service_fee",
            sa.Numeric(12, 2),
            nullable=False,
            server_default="0.00",
        ),
    )


def downgrade():
    op.drop_column("orders", "service_fee")
