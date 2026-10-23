from sqlalchemy import select

from app.agent.graph import graph
from app.database import SessionLocal
from app.models.case import ChargebackCaseModel


with SessionLocal() as session:
    statement = (
        select(ChargebackCaseModel.case_id)
        .order_by(ChargebackCaseModel.created_at.desc())
        .limit(1)
    )

    case_id = session.scalar(statement)


if case_id is None:
    raise RuntimeError("No chargeback case found")


print("CASE ID:")
print(case_id)


print("\nAGENT TRACE:")

for state in graph.stream(
    {
        "case_id": case_id,
    },
    config={
        "recursion_limit": 20,
    },
    stream_mode="values",
):
    messages = state.get("messages", [])

    if not messages:
        continue

    message = messages[-1]

    if getattr(message, "tool_calls", None):
        print(
            "TOOL CALLS:",
            message.tool_calls,
        )
    elif message.content:
        print(
            type(message).__name__,
            ":",
            message.content,
        )