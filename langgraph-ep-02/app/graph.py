from langgraph.graph import END, START, StateGraph

from app.nodes import (
    billing_help,
    classify_ticket,
    fallback,
    technical_help,
)
from app.routing import route_ticket
from app.state import TicketState

builder = StateGraph(TicketState)
builder.add_node("classify", classify_ticket)
builder.add_node("technical_help", technical_help)
builder.add_node("billing_help", billing_help)
builder.add_node("fallback", fallback)

builder.add_edge(START, "classify")
builder.add_conditional_edges(
    "classify",
    route_ticket,
    {
        "technical": "technical_help",
        "billing": "billing_help",
        "unknown": "fallback",
    },
)
builder.add_edge("technical_help", END)
builder.add_edge("billing_help", END)
builder.add_edge("fallback", END)

graph = builder.compile()
