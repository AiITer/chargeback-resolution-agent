from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Northstar Order Service")


class Order(BaseModel):
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

class StripeReferencesUpdate(BaseModel):
    payment_intent_id: str | None = None
    charge_id: str | None = None
    dispute_id: str | None = None

class OrderStatusUpdate(BaseModel):
    status: str

class OrderCreate(BaseModel):
    customer_id: str
    amount: int
    currency: str
    payment_intent_id: str
    created_at: datetime | None = None

class FulfillmentUpdate(BaseModel):
    fulfillment_status: str
    shipping_carrier: str | None = None
    tracking_number: str | None = None

class RefundUpdate(BaseModel):
    refund_status: str
    refund_amount: int
    refunded_at: datetime | None = None


ORDERS = {
    "ORDER-1001": Order(
        order_id="ORDER-1001",
        customer_id="CUSTOMER-1001",
        status="completed",
        created_at=datetime(2026, 10, 10, 14, 30, tzinfo=timezone.utc),
        amount=1800,
        currency="cad",
        fulfillment_status="shipped",
        shipping_carrier="shippo",
        tracking_number="SHIPPO_FAILURE",
        refund_status="refunded",
        refund_amount=1800,
        refunded_at=datetime(2026, 10, 22, 18, 0, tzinfo=timezone.utc),
        replacement_order_id=None,
    ),
    "ORDER-1002": Order(
        order_id="ORDER-1002",
        customer_id="CUSTOMER-1002",
        status="completed",
        created_at=datetime(
            2026, 10, 20, 14, 30,
            tzinfo=timezone.utc,
        ),
        amount=1800,
        currency="cad",
        fulfillment_status="shipped",
        shipping_carrier="shippo",
        tracking_number="SHIPPO_FAILURE",
        refund_status="refunded",
        refund_amount=1800,
        refunded_at=datetime(
            2026, 10, 22, 18, 0,
            tzinfo=timezone.utc,
        ),
        replacement_order_id=None,
    ),
    "ORDER-1003": Order(
        order_id="ORDER-1003",
        customer_id="CUSTOMER-1003",
        status="completed",
        created_at=datetime(
            2026, 10, 23, 12, 0,
            tzinfo=timezone.utc,
        ),
        amount=1800,
        currency="cad",

        payment_intent_id=None,
        charge_id=None,
        dispute_id=None,

        fulfillment_status="shipped",
        shipping_carrier="shippo",
        tracking_number="SHIPPO_FAILURE",

        refund_status="not_refunded",
        refund_amount=0,
        refunded_at=None,

        replacement_order_id=None,
    ),
}

def next_order_id() -> str:
    numbers = [
        int(order_id.split("-")[1])
        for order_id in ORDERS
    ]

    return f"ORDER-{max(numbers, default=1000) + 1}"

@app.post(
    "/orders",
    response_model=Order,
    status_code=201,
)
def create_order(payload: OrderCreate) -> Order:
    order_id = next_order_id()

    order = Order(
        order_id=order_id,
        customer_id=payload.customer_id,
        status="pending_payment",
        created_at=payload.created_at or datetime.now(timezone.utc),

        amount=payload.amount,
        currency=payload.currency,

        payment_intent_id=payload.payment_intent_id,
        charge_id=None,
        dispute_id=None,

        fulfillment_status="unfulfilled",
        shipping_carrier=None,
        tracking_number=None,

        refund_status="not_refunded",
        refund_amount=0,
        refunded_at=None,

        replacement_order_id=None,
    )

    ORDERS[order_id] = order

    return order


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str) -> Order:
    order = ORDERS.get(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order {order_id} not found",
        )

    return order

@app.patch(
    "/orders/{order_id}/stripe-references",
    response_model=Order,
)
def update_stripe_references(
    order_id: str,
    payload: StripeReferencesUpdate,
) -> Order:
    order = ORDERS.get(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order {order_id} not found",
        )

    if payload.payment_intent_id is not None:
        order.payment_intent_id = payload.payment_intent_id

    if payload.charge_id is not None:
        order.charge_id = payload.charge_id

    if payload.dispute_id is not None:
        order.dispute_id = payload.dispute_id

    return order

@app.get("/orders/lookup/stripe", response_model=Order)
def get_order_by_stripe_reference(
    payment_intent_id: str | None = None,
    charge_id: str | None = None,
) -> Order:
    if payment_intent_id is None and charge_id is None:
        raise HTTPException(
            status_code=400,
            detail="payment_intent_id or charge_id is required",
        )

    for order in ORDERS.values():
        if (
            payment_intent_id is not None
            and order.payment_intent_id == payment_intent_id
        ):
            return order

        if (
            charge_id is not None
            and order.charge_id == charge_id
        ):
            return order

    raise HTTPException(
        status_code=404,
        detail="Order not found for Stripe reference",
    )

@app.patch(
    "/orders/{order_id}/status",
    response_model=Order,
)
def update_order_status(
    order_id: str,
    payload: OrderStatusUpdate,
) -> Order:
    order = ORDERS.get(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order {order_id} not found",
        )

    order.status = payload.status

    return order

@app.patch(
    "/orders/{order_id}/fulfillment",
    response_model=Order,
)
def update_fulfillment(
    order_id: str,
    payload: FulfillmentUpdate,
) -> Order:
    order = ORDERS.get(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order {order_id} not found",
        )

    order.fulfillment_status = payload.fulfillment_status
    order.shipping_carrier = payload.shipping_carrier
    order.tracking_number = payload.tracking_number

    return order

@app.patch(
    "/orders/{order_id}/refund",
    response_model=Order,
)
def update_refund(
    order_id: str,
    payload: RefundUpdate,
) -> Order:
    order = ORDERS.get(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order {order_id} not found",
        )

    order.refund_status = payload.refund_status
    order.refund_amount = payload.refund_amount
    order.refunded_at = payload.refunded_at

    return order