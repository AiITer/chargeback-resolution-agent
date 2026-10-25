from typing import Literal

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from app.agent.nodes import (
    TOOLS,
    analyze_decision,
    assess_case,
    investigate,
    load_case_context,
    prepare_evidence,
    validate_submission,
)
from langchain_core.messages import ToolMessage
from app.agent.schemas import InvestigationDecision
from app.agent.state import ChargebackAgentState


tool_node = ToolNode(TOOLS)

def route_after_investigation(
    state: ChargebackAgentState,
) -> Literal["tools", "analyze_decision"]:
    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return "analyze_decision"

# def route_after_assessment(
#     state: ChargebackAgentState,
# ) -> Literal["__end__"]:
#     return "__end__"

# def route_after_assessment(
#     state: ChargebackAgentState,
# ) -> Literal["prepare_evidence", "__end__"]:
#     assessment = state["case_assessment"]

#     if (
#         assessment.decision
#         == InvestigationDecision.RECOMMEND_CONTEST
#     ):
#         return "prepare_evidence"

#     return END

def route_after_assessment(
    state: ChargebackAgentState,
) -> Literal["investigate", "__end__"]:
    assessment = state["case_assessment"]

    if assessment.decision == InvestigationDecision.CONTINUE_INVESTIGATION:
        return "investigate"

    return "__end__"


builder = StateGraph(ChargebackAgentState)

builder.add_node(
    "load_case_context",
    load_case_context,
)

builder.add_node(
    "investigate",
    investigate,
)

builder.add_node(
    "assess_case",
    assess_case,
)

builder.add_node(
    "prepare_evidence",
    prepare_evidence,
)

builder.add_node(
    "tools",
    tool_node,
)

builder.add_node(
    "validate_submission",
    validate_submission,
)

builder.add_node("analyze_decision", analyze_decision)

builder.add_edge(
    START,
    "load_case_context",
)

builder.add_edge(
    "load_case_context",
    "investigate",
)

builder.add_conditional_edges(
    "investigate",
     route_after_investigation,
)

builder.add_edge(
    "tools",
    "investigate",
)

builder.add_edge("analyze_decision", "assess_case")

builder.add_conditional_edges(
    "assess_case",
    route_after_assessment,
)

builder.add_edge(
    "prepare_evidence",
    "validate_submission",
)

builder.add_edge(
    "validate_submission",
    END,
)

graph = builder.compile()