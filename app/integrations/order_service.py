from datetime import datetime

import httpx
from pydantic import BaseModel

from app.config import settings


class OrderRecord(BaseModel):
    order_id: str
    customer_id: str
    status: str
    created_at: datetime

    fulfillment_status: str
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