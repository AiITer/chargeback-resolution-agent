from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field


class CaseStatus(StrEnum):
    OPEN = "open"
    GATHERING_EVIDENCE = "gathering_evidence"
    WAITING_FOR_HUMAN = "waiting_for_human"
    SUBMITTED = "submitted"
    WAITING_FOR_STRIPE = "waiting_for_stripe"
    WON = "won"
    LOST = "lost"
    CLOSED = "closed"

class ChargebackCaseCreate(BaseModel):
    case_id: str
    stripe_dispute_id: str
    dispute_reason: str

    amount: int = Field(ge=0)

    currency: str = Field(
        min_length=3,
        max_length=3,
    )

class CaseStatusUpdate(BaseModel):
    status: CaseStatus


class ChargebackCase(BaseModel):
    case_id: str
    stripe_dispute_id: str
    dispute_reason: str

    amount: int = Field(
        ge=0,
        description="Disputed amount in the smallest currency unit, for example cents.",
    )

    currency: str = Field(
        min_length=3,
        max_length=3,
    )

    status: CaseStatus = CaseStatus.OPEN

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )