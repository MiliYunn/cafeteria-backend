"""Configurable order fee calculations shared by customer and shop portals."""

from dataclasses import dataclass
from decimal import Decimal

from flask import current_app


@dataclass(frozen=True, slots=True)
class OrderFees:
    subtotal_amount: Decimal
    tax_fee: Decimal
    service_fee: Decimal
    total_amount: Decimal


class OrderFeeService:
    @staticmethod
    def configuration() -> dict[str, str]:
        settings = current_app.config["SETTINGS"]
        return {
            "tax_fee": format(settings.order_tax_fee, ".2f"),
            "pickup_service_fee": "0.00",
            "delivery_service_fee": format(
                settings.order_delivery_service_fee, ".2f"
            ),
        }

    @staticmethod
    def calculate(subtotal: Decimal, fulfillment: str) -> OrderFees:
        settings = current_app.config["SETTINGS"]
        clean_subtotal = subtotal.quantize(Decimal("0.01"))
        tax_fee = settings.order_tax_fee
        service_fee = (
            Decimal("0.00")
            if fulfillment == "pickup"
            else settings.order_delivery_service_fee
        )
        return OrderFees(
            subtotal_amount=clean_subtotal,
            tax_fee=tax_fee,
            service_fee=service_fee,
            total_amount=(clean_subtotal + tax_fee + service_fee).quantize(
                Decimal("0.01")
            ),
        )
