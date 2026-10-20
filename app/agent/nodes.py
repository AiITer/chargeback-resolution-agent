from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.prompts import CHARGEBACK_AGENT_SYSTEM_PROMPT
from app.agent.state import ChargebackAgentState
from app.agent.tools import search_company_knowledge
from app.database import SessionLocal
from app.integrations.llm import get_chat_model
from app.repositories.case import get_case_by_id

from datetime import datetime, timezone


TOOLS = [
    search_company_knowledge,
]

model = get_chat_model().bind_tools(TOOLS)


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


def investigate(state: ChargebackAgentState) -> dict:
    messages = state.get("messages", [])
    current_time = datetime.now(timezone.utc)

    if not messages:
        initial_messages = [
            SystemMessage(
                content=CHARGEBACK_AGENT_SYSTEM_PROMPT
            ),
            HumanMessage(
                content=(
                    "Investigate this formal dispute.\n\n"
                    f"Current time: {current_time.isoformat()}\n"
                    f"Stripe dispute ID: {state['stripe_dispute_id']}\n"
                    f"Stripe charge ID: {state.get('stripe_charge_id')}\n"
                    f"Payment intent ID: {state.get('stripe_payment_intent_id')}\n"
                    f"Dispute reason: {state['dispute_reason']}\n"
                    f"Amount: {state['amount']} {state['currency']}\n"
                    f"Stripe dispute status: {state.get('stripe_dispute_status')}\n"
                    f"Network reason code: {state.get('network_reason_code')}\n"
                    f"Evidence due by: {state.get('evidence_due_by')}"
                )
            ),
        ]

        response = model.invoke(initial_messages)

        return {
            "messages": [
                *initial_messages,
                response,
            ]
        }

    response = model.invoke(messages)

    return {
        "messages": [response]
    }