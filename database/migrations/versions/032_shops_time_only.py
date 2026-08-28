"""Store shop opening and closing hours as local times.

Upgrade retains the clock portion and NULL values, discarding calendar dates.
Back up shops before applying: the original dates cannot be reconstructed.
Downgrade restores DATETIME columns using 1970-01-01 as an explicit placeholder
date, NOT the discarded original dates. created_at and updated_at are preserved.
"""

from alembic import op
import sqlalchemy as sa

revision = "032_shops_time_only"
down_revision = "031_payment_accounts_shop"
branch_labels = None
depends_on = None


def upgrade():
    # MySQL's DATETIME -> TIME conversion keeps the time and drops the date.
    for column in ("open_at", "close_at"):
        op.alter_column(
            "shops", column, existing_type=sa.DateTime(), type_=sa.Time(),
            existing_nullable=True,
        )


def downgrade():
    for column in ("open_at", "close_at"):
        op.alter_column(
            "shops", column, existing_type=sa.Time(), type_=sa.DateTime(),
            existing_nullable=True,
        )
        # Override MySQL's implicit current-date conversion deterministically.
        op.execute(sa.text(
            f"UPDATE shops SET {column} = TIMESTAMP('1970-01-01', TIME({column})), "
            f"updated_at = updated_at WHERE {column} IS NOT NULL"
        ))
