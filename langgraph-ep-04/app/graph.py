from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.nodes import make_call_model
from app.tools import get_ticket_status


def build_graph(model, tools=None, system=None):
    available = tools if tools is not None else [get_ticket_status]
    call_model = make_call_model(model, **({"system": system} if system else {}))
    tool_node = ToolNode(available)
    builder = StateGraph(MessagesState)
    builder.add_node("agent", call_model)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "agent")
    builder.add_conditional_edges(
        "agent", tools_condition, {"tools": "tools", "__end__": END}
    )
    builder.add_edge("tools", "agent")
    return builder.compile()
