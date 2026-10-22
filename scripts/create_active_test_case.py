from datetime import datetime, timezone

from app.database import SessionLocal
from app.models.case import ChargebackCaseModel
from app.schemas.case import CaseStatus


CASE_ID = "11111111-1111-4111-8111-111111111111"


def main() -> None:
    with SessionLocal() as session:
        case = session.get(ChargebackCaseModel, CASE_ID)

        if case is None:
            case = ChargebackCaseModel(
                case_id=CASE_ID,
                stripe_dispute_id="du_test_active_001",
                stripe_charge_id="ch_test_active_001",
                stripe_payment_intent_id="pi_test_active_001",
                order_id="ORDER-1001",
                dispute_reason="product_not_received",
                amount=1800,
                currency="cad",
                stripe_dispute_status="needs_response",
                network_reason_code="13.1",
                evidence_due_by=datetime(
                    2026,
                    10,
                    25,
                    23,
                    59,
                    59,
                    tzinfo=timezone.utc,
                ),
                stripe_dispute_created_at=datetime(
                    2026,
                    10,
                    21,
                    12,
                    0,
                    tzinfo=timezone.utc,
                ),
                status=CaseStatus.OPEN,
            )

            session.add(case)

        else:
            case.order_id = "ORDER-1001"
            case.evidence_due_by = datetime(
                2026,
                10,
                25,
                23,
                59,
                59,
                tzinfo=timezone.utc,
            )
            case.status = CaseStatus.OPEN

        session.commit()

        print("CASE ID:", case.case_id)
        print("ORDER ID:", case.order_id)
        print("DEADLINE:", case.evidence_due_by)


if __name__ == "__main__":
    main()