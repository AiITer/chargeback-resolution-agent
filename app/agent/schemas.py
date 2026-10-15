from enum import StrEnum

from pydantic import BaseModel, Field


class InvestigationDecision(StrEnum):
    CONTINUE_INVESTIGATION = "continue_investigation"
    RECOMMEND_ACCEPT = "recommend_accept"
    RECOMMEND_CONTEST = "recommend_contest"
    NEEDS_HUMAN_REVIEW = "needs_human_review"


class CaseAssessment(BaseModel):
    decision: InvestigationDecision
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning_summary: str