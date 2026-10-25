from datetime import datetime

import httpx
from pydantic import BaseModel

from app.config import settings


class OrderRecord(BaseModel):
    order_id: str
    customer_id: str
    status: str
    created_at: datetime

    amount: int
    currency: str

    payment_intent_id: str | None = None
    charge_id: str | None = None
    dispute_id: str | None = None

    fulfillment_status: str
    shipping_carrier: str | None
    tracking_number: str | None

    refund_status: str
    refund_amount: int
    refunded_at: datetime | None

    replacement_order_id: str | None


def get_order(order_id: str) -> OrderRecord:
    response = httpx.get(
        f"{settings.order_service_base_url}/orders/{order_id}",
        timeout=5.0,
    )

    response.raise_for_status()

    return OrderRecord.model_validate(response.json())

def create_order(
    customer_id: str,
    amount: int,
    currency: str,
    payment_intent_id: str,
    created_at: datetime | None = None,
) -> OrderRecord:
    response = httpx.post(
        f"{settings.order_service_base_url}/orders",
        json={
            "customer_id": customer_id,
            "amount": amount,
            "currency": currency,
            "payment_intent_id": payment_intent_id,
            "created_at": (
                created_at.isoformat()
                if created_at is not None
                else None
            ),
        },
        timeout=5.0,
    )

    response.raise_for_status()

    return OrderRecord.model_validate(response.json())

def update_order_stripe_references(
    order_id: str,
    payment_intent_id: str | None = None,
    charge_id: str | None = None,
    dispute_id: str | None = None,
) -> OrderRecord:
    payload = {}

    if payment_intent_id is not None:
        payload["payment_intent_id"] = payment_intent_id

    if charge_id is not None:
        payload["charge_id"] = charge_id

    if dispute_id is not None:
        payload["dispute_id"] = dispute_id

    response = httpx.patch(
        f"{settings.order_service_base_url}"
        f"/orders/{order_id}/stripe-references",
        json=payload,
        timeout=5.0,
    )

    response.raise_for_status()

    return OrderRecord.model_validate(response.json())

def update_order_status(
    order_id: str,
    status: str,
) -> OrderRecord:
    response = httpx.patch(
        f"{settings.order_service_base_url}/orders/{order_id}/status",
        json={
            "status": status,
        },
        timeout=5.0,
    )

    response.raise_for_status()

    return OrderRecord.model_validate(response.json())

def find_order_by_stripe_reference(
    payment_intent_id: str | None = None,
    charge_id: str | None = None,
) -> OrderRecord:
    params = {}

    if payment_intent_id is not None:
        params["payment_intent_id"] = payment_intent_id

    if charge_id is not None:
        params["charge_id"] = charge_id

    response = httpx.get(
        f"{settings.order_service_base_url}/orders/lookup/stripe",
        params=params,
        timeout=5.0,
    )

    response.raise_for_status()

    return OrderRecord.model_validate(response.json())

def update_order_fulfillment(
    order_id: str,
    fulfillment_status: str,
    shipping_carrier: str | None = None,
    tracking_number: str | None = None,
) -> OrderRecord:
    response = httpx.patch(
        f"{settings.order_service_base_url}/orders/{order_id}/fulfillment",
        json={
            "fulfillment_status": fulfillment_status,
            "shipping_carrier": shipping_carrier,
            "tracking_number": tracking_number,
        },
        timeout=5.0,
    )

    response.raise_for_status()

    return OrderRecord.model_validate(response.json())

def update_order_refund(
    order_id: str,
    refund_status: str,
    refund_amount: int,
    refunded_at: datetime | None,
) -> OrderRecord:
    response = httpx.patch(
        f"{settings.order_service_base_url}/orders/{order_id}/refund",
        json={
            "refund_status": refund_status,
            "refund_amount": refund_amount,
            "refunded_at": (
                refunded_at.isoformat()
                if refunded_at is not None
                else None
            ),
        },
        timeout=5.0,
    )

    response.raise_for_status()

    return OrderRecord.model_validate(response.json())