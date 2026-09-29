from sqlalchemy.orm import Session

from app.models.case import ChargebackCaseModel


def add_case(
    session: Session,
    case: ChargebackCaseModel,
) -> ChargebackCaseModel:
    session.add(case)
    return case