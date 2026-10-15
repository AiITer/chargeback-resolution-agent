from datetime import datetime
from typing import TypedDict

from app.agent.schemas import CaseAssessment


class ChargebackAgentState(TypedDict, total=False):
    case_id: str

    stripe_dispute_id: str
    stripe_charge_id: str | None
    stripe_payment_intent_id: str | None

    dispute_reason: str
    amount: int
    currency: str

    stripe_dispute_status: str | None
    network_reason_code: str | None
    evidence_due_by: datetime | None

    case_assessment: CaseAssessment