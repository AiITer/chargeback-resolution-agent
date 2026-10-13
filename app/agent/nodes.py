from app.agent.state import ChargebackAgentState
from app.database import SessionLocal
from app.repositories.case import get_case_by_id


def load_case_context(state: ChargebackAgentState) -> dict:
    case_id = state["case_id"]

    with SessionLocal() as session:
        case = get_case_by_id(session, case_id)

        if case is None:
            raise ValueError(f"Case not found: {case_id}")

        return {
            "stripe_dispute_id": case.stripe_dispute_id,
            "stripe_charge_id": case.stripe_charge_id,
            "stripe_payment_intent_id": case.stripe_payment_intent_id,
            "dispute_reason": case.dispute_reason,
            "amount": case.amount,
            "currency": case.currency,
            "stripe_dispute_status": case.stripe_dispute_status,
            "network_reason_code": case.network_reason_code,
            "evidence_due_by": case.evidence_due_by,
        }