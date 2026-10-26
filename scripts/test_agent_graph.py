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

final_state = None

for state in graph.stream(
    {
        "case_id": case_id,
        "stripe_test_outcome": "won",
    },
    config={
        "recursion_limit": 30,
    },
    stream_mode="values",
):
    final_state = state
            
    assessment = state.get("case_assessment")

    if assessment is not None:
        print("\nCASE ASSESSMENT:")
        print("DECISION:", assessment.decision)
        print("CONFIDENCE:", assessment.confidence)
        print("REASONING:", assessment.reasoning_summary)

    evidence = state.get("evidence_package")

    if evidence is not None:
        print("\nEVIDENCE PACKAGE:")
        print(
            "UNCATEGORIZED TEXT:",
            evidence.uncategorized_text,
        )
        print(
            "SHIPPING CARRIER:",
            evidence.shipping_carrier,
        )
        print(
            "TRACKING NUMBER:",
            evidence.shipping_tracking_number,
        )

    validation = state.get("stage_validation")

    if validation is not None:
        print("\nSTAGE VALIDATION:")
        print("IS VALID:", validation.is_valid)
        print("ERRORS:", validation.errors)

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

decision_analysis = final_state.get("decision_analysis")

print("\nDECISION ANALYSIS:")

if decision_analysis is None:
    print("None")
else:
    print("\nMATERIAL FACTS:")
    for index, fact in enumerate(decision_analysis.material_facts, start=1):
        print(f"{index}. {fact}")

    print("\nRELEVANT POLICY:")
    for index, policy in enumerate(decision_analysis.relevant_policy, start=1):
        print(f"{index}. {policy}")

    print("\nUNRESOLVED GAPS:")
    if decision_analysis.unresolved_gaps:
        for index, gap in enumerate(decision_analysis.unresolved_gaps, start=1):
            print(f"{index}. {gap}")
    else:
        print("None")