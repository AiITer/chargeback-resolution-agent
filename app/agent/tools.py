from dataclasses import asdict

from langchain_core.tools import tool
from app.integrations.order_service import get_order

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
        f"Tracking number: {order.tracking_number}\n"
        f"Refund status: {order.refund_status}\n"
        f"Refund amount: {order.refund_amount}\n"
        f"Refunded at: "
        f"{order.refunded_at.isoformat() if order.refunded_at else None}\n"
        f"Replacement order ID: {order.replacement_order_id}"
    )

    artifact = order.model_dump(mode="json")

    return content, artifact