from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from app.agent.prompts import CHARGEBACK_AGENT_SYSTEM_PROMPT
from app.agent.schemas import (
    CaseAssessment,
    EvidencePackage,
    SubmissionValidation,
    DecisionAnalysis,
    InvestigationDecision
)

from app.integrations.order_service import get_order
from app.integrations.stripe import get_stripe_dispute

from app.agent.state import ChargebackAgentState
from app.agent.tools import (
    get_order_details,
    get_tracking_details,
    search_company_knowledge,
)
from app.database import SessionLocal
from app.integrations.llm import get_chat_model
from app.repositories.case import get_case_by_id

from datetime import datetime, timezone


TOOLS = [
    search_company_knowledge,   
    get_order_details,
    get_tracking_details,
]

model = get_chat_model().bind_tools(TOOLS)
assessment_model = get_chat_model().with_structured_output(
    CaseAssessment
)
evidence_model = get_chat_model().with_structured_output(
    EvidencePackage
)
analysis_model = get_chat_model().with_structured_output(DecisionAnalysis)

MAX_INVESTIGATION_TOOL_RESULTS = 10

def load_case_context(state: ChargebackAgentState) -> dict:
    case_id = state["case_id"]

    with SessionLocal() as session:
        case = get_case_by_id(session, case_id)

        if case is None:
            raise ValueError(f"Case not found: {case_id}")

        return {
            "order_id": case.order_id,
            "stripe_dispute_id": case.stripe_dispute_id,
            "stripe_charge_id": case.stripe_charge_id,
            "stripe_payment_intent_id": case.stripe_payment_intent_id,
            "dispute_reason": case.dispute_reason,
            "amount": case.amount,
            "currency": case.currency,
            "stripe_dispute_status": case.stripe_dispute_status,
            "network_reason_code": case.network_reason_code,
            "evidence_due_by": case.evidence_due_by,
            "stripe_dispute_created_at": case.stripe_dispute_created_at,
        }


def investigate(state: ChargebackAgentState) -> dict:
    messages = state.get("messages", [])
    current_time = datetime.now(timezone.utc)

    tool_result_count = sum(
        isinstance(message, ToolMessage)
        for message in messages
    )

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
                    f"Order ID: {state.get('order_id')}\n"
                    f"Dispute reason: {state['dispute_reason']}\n"
                    f"Amount: {state['amount']} {state['currency']}\n"
                    f"Stripe dispute status: {state.get('stripe_dispute_status')}\n"
                    f"Network reason code: {state.get('network_reason_code')}\n"
                    f"Stripe dispute created at: {state.get('stripe_dispute_created_at')}\n"
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

    if tool_result_count >= MAX_INVESTIGATION_TOOL_RESULTS:
        return {}

def assess_case(state):
    messages = state["messages"]
    analysis = state["decision_analysis"]

    assessment = assessment_model.invoke(
        [
            *messages,
            HumanMessage(
                content=(
                    "Based on the investigation and the structured summary below, "
                    "produce the final case assessment.\n\n"
                    f"Material facts: {analysis.material_facts}\n"
                    f"Relevant policy: {analysis.relevant_policy}\n"
                    f"Unresolved gaps: {analysis.unresolved_gaps}\n\n"
                    "Do not gather new evidence. "
                    "Choose the next investigation decision."
                )
            ),
        ]
    )

    result = {"case_assessment": assessment}

    if assessment.decision == InvestigationDecision.CONTINUE_INVESTIGATION:
        result["messages"] = [
            HumanMessage(
                content=(
                    "Continue the investigation based on the unresolved gaps "
                    "identified in the assessment. Use the available tools to "
                    "retrieve specific missing information that could materially "
                    "change or strengthen the decision. Do not simply repeat the "
                    "previous investigation or the previous conclusion."
                )
            )
        ]

    return result

def prepare_evidence(
    state: ChargebackAgentState,
) -> dict:
    assessment = state["case_assessment"]

    if assessment.decision != "recommend_contest":
        raise ValueError(
            "Evidence package can only be prepared "
            "for a contest recommendation."
        )

    evidence = evidence_model.invoke(
        [
            *state["messages"],
            HumanMessage(
                content=(
                    "Prepare the Stripe evidence package for this dispute. "
                    "Use only facts established during the investigation "
                    "and the final case assessment. "
                    f"Final assessment reasoning: "
                    f"{assessment.reasoning_summary}\n"
                    "Select evidence that directly supports the contest "
                    "recommendation. "
                    "Do not invent facts or make claims unsupported by "
                    "the investigation. "
                    "Return concise evidence suitable for an external "
                    "dispute reviewer."
                )
            ),
        ]
    )

    return {
        "evidence_package": evidence,
    }

def validate_submission(
    state: ChargebackAgentState,
) -> dict:
    errors: list[str] = []

    assessment = state["case_assessment"]
    evidence = state["evidence_package"]

    order_id = state.get("order_id")

    if order_id is None:
        errors.append("Case has no associated order.")
    else:
        order = get_order(order_id)

        if order.payment_intent_id != state.get(
            "stripe_payment_intent_id"
        ):
            errors.append(
                "Order PaymentIntent does not match the Case."
            )

        if order.charge_id != state.get(
            "stripe_charge_id"
        ):
            errors.append(
                "Order Charge does not match the Case."
            )

        if order.dispute_id != state.get(
            "stripe_dispute_id"
        ):
            errors.append(
                "Order dispute does not match the Case."
            )

        if (
            evidence.shipping_carrier is not None
            and evidence.shipping_carrier
            != order.shipping_carrier
        ):
            errors.append(
                "Evidence shipping carrier does not match "
                "the Order."
            )

        if (
            evidence.shipping_tracking_number is not None
            and evidence.shipping_tracking_number
            != order.tracking_number
        ):
            errors.append(
                "Evidence tracking number does not match "
                "the Order."
            )

    dispute = get_stripe_dispute(
        state["stripe_dispute_id"]
    ).to_dict()

    if dispute.get("id") != state["stripe_dispute_id"]:
        errors.append(
            "Stripe dispute ID does not match the Case."
        )

    if dispute.get("charge") != state.get(
        "stripe_charge_id"
    ):
        errors.append(
            "Stripe dispute Charge does not match the Case."
        )

    if dispute.get("payment_intent") != state.get(
        "stripe_payment_intent_id"
    ):
        errors.append(
            "Stripe dispute PaymentIntent does not match "
            "the Case."
        )

    evidence_due_by = state.get("evidence_due_by")

    if (
        evidence_due_by is not None
        and datetime.now(timezone.utc) >= evidence_due_by
    ):
        errors.append(
            "Stripe evidence deadline has passed."
        )
    if dispute.get("status") != "needs_response":
        errors.append(
            "Stripe dispute is not in needs_response status."
        )
    if not evidence.uncategorized_text.strip():
        errors.append(
            "Evidence text is empty."
        )
    if assessment.decision != "recommend_contest":
        errors.append(
            "Case assessment does not recommend contest."
        )

    validation = SubmissionValidation(
        is_valid=len(errors) == 0,
        errors=errors,
    )

    return {
        "submission_validation": validation,
    }

def analyze_decision(state):
    messages = state["messages"]

    analysis = analysis_model.invoke(
        [
            *messages,
            HumanMessage(
                content=(
                    "Summarize the completed investigation. "
                    "Identify the material case facts, the relevant retrieved "
                    "policy or guidance, and any unresolved information gaps. "
                    "Do not make a final recommendation."
                )
            ),
        ]
    )

    return {"decision_analysis": analysis}