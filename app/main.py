from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import uuid4

from app.database import get_db
from app.repositories.case import (
    add_case,
    get_case_by_id,
    get_case_by_stripe_dispute_id,
    update_case_status,
)

from app.models.case import ChargebackCaseModel
from app.schemas.case import (
    ChargebackCase,
    ChargebackCaseCreate,
    CaseStatusUpdate,
)

from app.integrations.stripe import construct_stripe_event

app = FastAPI(
    title="Chargeback Resolution Agent",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/cases/{case_id}", response_model=ChargebackCase)
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

@app.get(
    "/cases/stripe/{stripe_dispute_id}",
    response_model=ChargebackCase,
)
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

@app.post(
    "/cases",
    response_model=ChargebackCase,
    status_code=201,
)
def create_case(
    payload: ChargebackCaseCreate,
    session: Session = Depends(get_db),
):
    case = ChargebackCaseModel(
        case_id=str(uuid4()),
        **payload.model_dump()
    )

    add_case(session, case)
    
    try:
        session.commit()

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Case already exists",
        )

    session.refresh(case)
    return case

@app.patch(
    "/cases/{case_id}/status",
    response_model=ChargebackCase,
)
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

@app.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    session: Session = Depends(get_db),
):
    payload = await request.body()
    signature = request.headers.get("stripe-signature")

    try:
        event = construct_stripe_event(
            payload,
            signature,
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid Stripe webhook signature",
        )

    if event["type"] == "charge.dispute.created":
        dispute = event["data"]["object"]

        case = get_case_by_stripe_dispute_id(
            session,
            dispute["id"],
        )

        if case is None:
            case = ChargebackCaseModel(
                case_id=str(uuid4()),
                stripe_dispute_id=dispute["id"],
                dispute_reason=dispute["reason"],
                amount=dispute["amount"],
                currency=dispute["currency"],
            )

            add_case(session, case)
            session.commit()
            session.refresh(case)

            print("Created case:", case.case_id)
            
    return {"received": True}