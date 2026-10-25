from typing import Literal

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from app.agent.nodes import (
    TOOLS,
    assess_case,
    investigate,
    load_case_context,
    prepare_evidence,
)

from app.agent.schemas import InvestigationDecision
from app.agent.state import ChargebackAgentState


tool_node = ToolNode(TOOLS)


def route_after_investigate(
    state: ChargebackAgentState,
) -> Literal["tools", "assess_case"]:
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "assess_case"

def route_after_assessment(
    state: ChargebackAgentState,
) -> Literal["prepare_evidence", "__end__"]:
    assessment = state["case_assessment"]

    if (
        assessment.decision
        == InvestigationDecision.RECOMMEND_CONTEST
    ):
        return "prepare_evidence"

    return END


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
    route_after_investigate,
)

builder.add_edge(
    "tools",
    "investigate",
)

builder.add_conditional_edges(
    "assess_case",
    route_after_assessment,
)

builder.add_edge(
    "prepare_evidence",
    END,
)

graph = builder.compile()