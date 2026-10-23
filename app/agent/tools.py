from dataclasses import asdict

from langchain_core.tools import tool
from app.integrations.order_service import get_order
from app.integrations.shippo import get_tracking

from app.config import settings
from app.rag.retrieval import (
    format_knowledge_results,
    search_knowledge,
)


@tool(response_format="content_and_artifact")
def search_company_knowledge(query: str):
    """Search approved company policy and long-lived dispute guidance.

    Use this tool for policy, authority, evidence requirements, and other
    stable chargeback guidance. Do not use it for live case facts such as
    current Stripe, order, shipment, or customer-message state.
    """
    results = search_knowledge(
        query,
        top_k=settings.knowledge_retrieval_top_k,
    )

    content = format_knowledge_results(results)
    artifact = [asdict(result) for result in results]

    return content, artifact

@tool(response_format="content_and_artifact")
def get_order_details(order_id: str):
    """Retrieve current operational order facts from Northstar Order Service.

    Use this tool for live order facts such as fulfillment status, tracking
    linkage, refund status, refund timing, and replacement-order linkage.
    Do not use this tool for company policy or dispute guidance.
    """
    order = get_order(order_id)

    content = (
        f"Order ID: {order.order_id}\n"
        f"Customer ID: {order.customer_id}\n"
        f"Status: {order.status}\n"
        f"Created at: {order.created_at.isoformat()}\n"
        f"Fulfillment status: {order.fulfillment_status}\n"
        f"Shipping carrier: {order.shipping_carrier}\n"
        f"Tracking number: {order.tracking_number}\n"
        f"Refund status: {order.refund_status}\n"
        f"Refund amount: {order.refund_amount}\n"
        f"Refunded at: "
        f"{order.refunded_at.isoformat() if order.refunded_at else None}\n"
        f"Replacement order ID: {order.replacement_order_id}"
    )

    artifact = order.model_dump(mode="json")

    return content, artifact

@tool(response_format="content_and_artifact")
def get_tracking_details(
    carrier: str,
    tracking_number: str,
):
    """Retrieve current shipment tracking facts from Shippo.

    Use this tool for live shipping facts such as current shipment status,
    delivery status, delivery timing, estimated arrival, and tracking history.
    Do not use this tool for company policy or order facts.
    """
    tracking = get_tracking(
        carrier=carrier,
        tracking_number=tracking_number,
    )

    event_lines = []

    for event in tracking.events:
        location_parts = []

        if event.location is not None:
            for value in (
                event.location.city,
                event.location.state,
                event.location.country,
                event.location.zip,
            ):
                if value:
                    location_parts.append(value)

        location_text = (
            f" | location: {', '.join(location_parts)}"
            if location_parts
            else ""
        )

        event_lines.append(
            f"- {event.occurred_at} | {event.status} | "
            f"{event.status_details}{location_text}"
        )

    content = (
        f"Tracking number: {tracking.tracking_number}\n"
        f"Carrier: {tracking.carrier}\n"
        f"Current status: {tracking.status}\n"
        f"Current status detail: {tracking.status_details}\n"
        f"Current status date: {tracking.status_date}\n"
        f"Estimated delivery time: {tracking.eta}\n"
        f"Tracking history:\n"
        + "\n".join(event_lines)
    )

    artifact = tracking.model_dump(mode="json")

    return content, artifact