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

class EvidencePackage(BaseModel):
    uncategorized_text: str

    shipping_carrier: str | None = None
    shipping_tracking_number: str | None = None

class StageValidation(BaseModel):
    is_valid: bool
    errors: list[str] = Field(default_factory=list)

class DecisionAnalysis(BaseModel):
    material_facts: list[str]
    relevant_policy: list[str]
    unresolved_gaps: list[str]