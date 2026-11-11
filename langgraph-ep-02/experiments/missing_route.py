"""The graph as it stands before the fallback route is added.

Run it from the episode folder to see the failure from the video:

    python -m experiments.missing_route
"""
from langgraph.graph import END, START, StateGraph

from app.nodes import billing_help, classify_ticket, technical_help
from app.routing import route_ticket
from app.state import TicketState

builder = StateGraph(TicketState)
builder.add_node("classify", classify_ticket)
builder.add_node("technical_help", technical_help)
builder.add_node("billing_help", billing_help)

builder.add_edge(START, "classify")
builder.add_conditional_edges(
    "classify",
    route_ticket,
    {
        "technical": "technical_help",
        "billing": "billing_help",
    },
)
builder.add_edge("technical_help", END)
builder.add_edge("billing_help", END)

graph = builder.compile()

if __name__ == "__main__":
    print(graph.invoke({"ticket": "hello"}))
