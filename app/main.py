from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.case import get_case_by_id

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