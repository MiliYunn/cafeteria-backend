from sqlalchemy import select

from extensions import db
from models.payment_method import PaymentMethod


def seed_payment_methods() -> None:
    existing = set(db.session.scalars(select(PaymentMethod.name)).all())
    defaults = (
        {"name": "Cash", "type": "cash", "description": "Pay when collecting the order"},
        {"name": "Online Transfer", "type": "bank_transfer", "description": "Pay to a configured bank account"},
    )
    db.session.add_all(PaymentMethod(**item) for item in defaults if item["name"] not in existing)
    db.session.commit()

