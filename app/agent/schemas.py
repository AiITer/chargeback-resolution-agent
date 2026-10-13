from enum import StrEnum

from pydantic import BaseModel, Field


class TriageDecision(StrEnum):
    WORTH_INVESTIGATING = "worth_investigating"
    RECOMMEND_ACCEPT = "recommend_accept"
    NEEDS_HUMAN_REVIEW = "needs_human_review"


class TriageResult(BaseModel):
    decision: TriageDecision
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning_summary: str