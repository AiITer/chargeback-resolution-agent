from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CaseStatus(StrEnum):
    OPEN = "open"
    GATHERING_EVIDENCE = "gathering_evidence"
    WAITING_FOR_HUMAN = "waiting_for_human"
    SUBMITTED = "submitted"
    WAITING_FOR_STRIPE = "waiting_for_stripe"
    WON = "won"
    LOST = "lost"
    CLOSED = "closed"

# DEV/ADMIN ONLY — not part of the production Agent workflow.
# class ChargebackCaseCreate(BaseModel):
#     stripe_dispute_id: str
#     dispute_reason: str

#     amount: int = Field(ge=0)

#     currency: str = Field(
#         min_length=3,
#         max_length=3,
#     )

# DEV/ADMIN ONLY — kept for manual workflow-state debugging.
# class CaseStatusUpdate(BaseModel):
#     status: CaseStatus


class ChargebackCase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    case_id: str
    stripe_dispute_id: str

    stripe_charge_id: str | None = None
    stripe_payment_intent_id: str | None = None

    dispute_reason: str

    amount: int = Field(
        ge=0,
        description="Disputed amount in the smallest currency unit, for example cents.",
    )

    currency: str = Field(
        min_length=3,
        max_length=3,
    )

    stripe_dispute_status: str | None = None
    network_reason_code: str | None = None
    evidence_due_by: datetime | None = None
    stripe_dispute_created_at: datetime | None = None

    status: CaseStatus = CaseStatus.OPEN

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    
    