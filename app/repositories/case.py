from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import ChargebackCaseModel
from app.schemas.case import CaseStatus


def add_case(
    session: Session,
    case: ChargebackCaseModel,
) -> ChargebackCaseModel:
    session.add(case)
    return case

def get_case_by_id(
    session: Session,
    case_id: str,
) -> ChargebackCaseModel | None:
    statement = (
        select(ChargebackCaseModel)
        .where(ChargebackCaseModel.case_id == case_id)
    )

    return session.scalar(statement)

def get_case_by_stripe_dispute_id(
    session: Session,
    stripe_dispute_id: str,
) -> ChargebackCaseModel | None:
    statement = (
        select(ChargebackCaseModel)
        .where(
            ChargebackCaseModel.stripe_dispute_id
            == stripe_dispute_id
        )
    )

    return session.scalar(statement)

def update_case_status(
    session: Session,
    case: ChargebackCaseModel,
    status: CaseStatus,
) -> ChargebackCaseModel:
    case.status = status
    session.add(case)
    return case

def update_case_assessment(
    session: Session,
    case: ChargebackCaseModel,
    *,
    decision: str,
    confidence: float,
    reasoning: str,
) -> ChargebackCaseModel:
    case.agent_decision = decision
    case.agent_confidence = confidence
    case.agent_reasoning = reasoning

    session.add(case)

    return case