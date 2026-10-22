from app.database import SessionLocal
from app.models.case import ChargebackCaseModel


CASE_ID = "4cfc84a7-86c9-4a4d-a980-fa696d39949c"
ORDER_ID = "ORDER-1001"


def main() -> None:
    with SessionLocal() as session:
        case = session.get(ChargebackCaseModel, CASE_ID)

        if case is None:
            raise RuntimeError(f"Case not found: {CASE_ID}")

        case.order_id = ORDER_ID
        session.commit()

        print("CASE ID:", case.case_id)
        print("ORDER ID:", case.order_id)


if __name__ == "__main__":
    main()