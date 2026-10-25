from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
import logging
from datetime import datetime, timezone

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
    # ChargebackCaseCreate,
    # CaseStatusUpdate,
)

from app.integrations.stripe import construct_stripe_event
from app.integrations.order_service import (
    find_order_by_stripe_reference,
    update_order_stripe_references,
)

logger = logging.getLogger("uvicorn.error")

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

# DEV/ADMIN ONLY — not part of the production Agent workflow.
# @app.post(
#     "/cases",
#     response_model=ChargebackCase,
#     status_code=201,
# )
# def create_case(
#     payload: ChargebackCaseCreate,
#     session: Session = Depends(get_db),
# ):
#     case = ChargebackCaseModel(
#         case_id=str(uuid4()),
#         **payload.model_dump()
#     )

#     add_case(session, case)
    
#     try:
#         session.commit()

#     except IntegrityError:
#         session.rollback()

#         raise HTTPException(
#             status_code=409,
#             detail="Case already exists",
#         )

#     session.refresh(case)
#     return case

# @app.patch(
#     "/cases/{case_id}/status",
#     response_model=ChargebackCase,
# )
# def patch_case_status(
#     case_id: str,
#     payload: CaseStatusUpdate,
#     session: Session = Depends(get_db),
# ):
#     case = get_case_by_id(session, case_id)

#     if case is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Case not found",
#         )

#     update_case_status(
#         session,
#         case,
#         payload.status,
#     )

#     session.commit()
#     session.refresh(case)

#     return case

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
        dispute = event["data"]["object"].to_dict()

        payment_intent_id = dispute.get("payment_intent")
        charge_id = dispute.get("charge")

        order = find_order_by_stripe_reference(
            payment_intent_id=payment_intent_id,
            charge_id=charge_id,
        )

        case = get_case_by_stripe_dispute_id(
            session,
            dispute["id"],
        )

        if case is None:
            payment_method_details = (
                dispute.get("payment_method_details") or {}
            )

            card_details = (
                payment_method_details.get("card") or {}
            )

            evidence_details = (
                dispute.get("evidence_details") or {}
            )

            due_by = evidence_details.get("due_by")
            stripe_created = dispute.get("created")
            case = ChargebackCaseModel(
                case_id=str(uuid4()),
                order_id=order.order_id,
                stripe_dispute_id=dispute["id"],
                stripe_charge_id=charge_id,
                stripe_payment_intent_id=payment_intent_id,
                dispute_reason=dispute["reason"],
                amount=dispute["amount"],
                currency=dispute["currency"],
                stripe_dispute_status=dispute.get("status"),
                network_reason_code=card_details.get("network_reason_code"),
                evidence_due_by=(
                    datetime.fromtimestamp(
                        due_by,
                        tz=timezone.utc,
                    )
                    if due_by is not None
                    else None
                ),
                stripe_dispute_created_at=(
                    datetime.fromtimestamp(
                        stripe_created,
                        tz=timezone.utc,
                    )
                    if stripe_created is not None
                    else None
                ),
            )

            add_case(session, case)
            session.commit()
            session.refresh(case)
            
            update_order_stripe_references(
                order.order_id,
                dispute_id=dispute["id"],
            )

            logger.info(
                "Created chargeback case %s from Stripe dispute %s",
                case.case_id,
                dispute["id"],
            )
            
    return {"received": True}