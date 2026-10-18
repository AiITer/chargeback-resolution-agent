from dataclasses import asdict

from langchain_core.tools import tool

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