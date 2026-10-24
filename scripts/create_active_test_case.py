from datetime import datetime, timezone

from app.database import SessionLocal
from app.models.case import ChargebackCaseModel
from app.schemas.case import CaseStatus


CASE_ID = "22222222-2222-4222-8222-222222222222"


def main() -> None:
    with SessionLocal() as session:
        case = session.get(ChargebackCaseModel, CASE_ID)

        if case is None:
            case = ChargebackCaseModel(
                case_id=CASE_ID,
                stripe_dispute_id="du_test_refund_first_002",
                stripe_charge_id="ch_test_refund_first_002",
                stripe_payment_intent_id="pi_test_refund_first_002",
                order_id="ORDER-1002",
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
                    23,
                    9,
                    0,
                    tzinfo=timezone.utc,
                ),
                status=CaseStatus.OPEN,
            )

            session.add(case)

        else:
            case.order_id = "ORDER-1002"
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
        print("DISPUTE CREATED AT:", case.stripe_dispute_created_at)
        print("DEADLINE:", case.evidence_due_by)


if __name__ == "__main__":
    main()