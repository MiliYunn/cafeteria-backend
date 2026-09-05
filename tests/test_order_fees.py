from decimal import Decimal

from services.shared.order_fee_service import OrderFeeService


def test_pickup_has_tax_but_no_service_fee(app):
    with app.app_context():
        fees = OrderFeeService.calculate(Decimal("12.50"), "pickup")

    assert fees.subtotal_amount == Decimal("12.50")
    assert fees.tax_fee == Decimal("1.00")
    assert fees.service_fee == Decimal("0.00")
    assert fees.total_amount == Decimal("13.50")


def test_delivery_adds_configured_service_fee(app):
    with app.app_context():
        fees = OrderFeeService.calculate(Decimal("12.50"), "delivery")

    assert fees.tax_fee == Decimal("1.00")
    assert fees.service_fee == Decimal("1.00")
    assert fees.total_amount == Decimal("14.50")
