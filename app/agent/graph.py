from typing import Literal

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from app.agent.nodes import (
    TOOLS,
    investigate,
    load_case_context,
)
from app.agent.state import ChargebackAgentState


tool_node = ToolNode(TOOLS)


def route_after_investigate(
    state: ChargebackAgentState,
) -> Literal["tools", "__end__"]:
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

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

graph = builder.compile()