from langgraph.graph import END, START, StateGraph

from app.nodes import (
    escalate_ticket,
    fetch_context,
)
from app.routing import route_after_fetch
from app.state import LookupState

builder = StateGraph(LookupState)
builder.add_node("fetch_context", fetch_context)
builder.add_node("escalate_ticket", escalate_ticket)

builder.add_edge(START, "fetch_context")
builder.add_conditional_edges(
    "fetch_context",
    route_after_fetch,
    {
        "done": END,
        "retry": "fetch_context",
        "escalate": "escalate_ticket",
    },
)
builder.add_edge("escalate_ticket", END)

graph = builder.compile()
