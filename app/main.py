from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.case import (
    add_case,
    get_case_by_id,
    get_case_by_stripe_dispute_id,
    update_case_status,
)

from app.models.case import ChargebackCaseModel
from app.schemas.case import (
    ChargebackCaseCreate,
    CaseStatusUpdate,
)

app = FastAPI(
    title="Chargeback Resolution Agent",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/cases/{case_id}")
def get_case(
    case_id: str,
    session: Session = Depends(get_db),
):
    case = get_case_by_id(session, case_id)

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found",
        )

    return case

@app.get("/cases/stripe/{stripe_dispute_id}")
def get_case_by_stripe(
    stripe_dispute_id: str,
    session: Session = Depends(get_db),
):
    case = get_case_by_stripe_dispute_id(
        session,
        stripe_dispute_id,
    )

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found",
        )

    return case

@app.post("/cases")
def create_case(
    payload: ChargebackCaseCreate,
    session: Session = Depends(get_db),
):
    case = ChargebackCaseModel(
        **payload.model_dump()
    )

    add_case(session, case)
    session.commit()
    session.refresh(case)

    return case

@app.patch("/cases/{case_id}/status")
def patch_case_status(
    case_id: str,
    payload: CaseStatusUpdate,
    session: Session = Depends(get_db),
):
    case = get_case_by_id(session, case_id)

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found",
        )

    update_case_status(
        session,
        case,
        payload.status,
    )

    session.commit()
    session.refresh(case)

    return case