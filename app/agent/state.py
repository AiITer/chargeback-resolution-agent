from datetime import datetime
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from app.agent.schemas import (
    CaseAssessment,
    EvidencePackage,
    SubmissionValidation,
    DecisionAnalysis,
)

class ChargebackAgentState(TypedDict, total=False):
    case_id: str
    order_id: str | None

    stripe_dispute_id: str
    stripe_charge_id: str | None
    stripe_payment_intent_id: str | None

    dispute_reason: str
    amount: int
    currency: str

    stripe_dispute_status: str | None
    network_reason_code: str | None
    evidence_due_by: datetime | None
    stripe_dispute_created_at: datetime | None

    messages: Annotated[list[AnyMessage], add_messages]

    case_assessment: CaseAssessment
    evidence_package: EvidencePackage
    submission_validation: SubmissionValidation
    decision_analysis: DecisionAnalysis | None