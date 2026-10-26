from concurrent.futures import ThreadPoolExecutor

from sqlalchemy import select

from app.agent.graph import graph
from app.database import SessionLocal
from app.models.case import ChargebackCaseModel
from app.schemas.case import CaseStatus


MAX_WORKERS = 2

def run_case(case_id: str) -> None:
    graph.invoke(
        {
            "case_id": case_id,
        },
        config={
            "recursion_limit": 30,
        },
        stream_mode="values",
    )

def get_pending_case_ids(limit: int) -> list[str]:
  with SessionLocal() as session:
      statement = (
          select(ChargebackCaseModel.case_id)
          .where(
              ChargebackCaseModel.status
              == CaseStatus.OPEN,
              ChargebackCaseModel.order_id.is_not(None),
          )
          .order_by(
              ChargebackCaseModel.created_at.asc()
          )
          .limit(limit)
      )

      return list(
          session.scalars(statement).all()
      )

def run_scheduler_once() -> None:
  case_ids = get_pending_case_ids(MAX_WORKERS)

  if not case_ids:
      return

  with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        futures = [
            executor.submit(
                run_case,
                case_id,
            )
            for case_id in case_ids
        ]

        for future in futures:
            future.result()