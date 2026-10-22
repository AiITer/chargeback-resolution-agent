from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Northstar Order Service")


class Order(BaseModel):
    order_id: str
    customer_id: str
    status: str
    created_at: datetime

    fulfillment_status: str
    shipping_carrier: str | None
    tracking_number: str | None

    refund_status: str
    refund_amount: int
    refunded_at: datetime | None

    replacement_order_id: str | None


ORDERS = {
    "ORDER-1001": Order(
        order_id="ORDER-1001",
        customer_id="CUSTOMER-1001",
        status="completed",
        created_at=datetime(2026, 10, 10, 14, 30, tzinfo=timezone.utc),
        fulfillment_status="shipped",
        shipping_carrier="shippo",
        tracking_number="SHIPPO_DELIVERED",
        refund_status="not_refunded",
        refund_amount=0,
        refunded_at=None,
        replacement_order_id=None,
    )
}


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str) -> Order:
    order = ORDERS.get(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail=f"Order {order_id} not found",
        )

    return order