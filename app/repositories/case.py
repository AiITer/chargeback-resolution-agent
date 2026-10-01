from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import ChargebackCaseModel


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