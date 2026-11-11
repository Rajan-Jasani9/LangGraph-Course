"""A cycle with no retry limit, run against a service that never recovers.

LangGraph's default recursion limit is very high (about 10,000 steps in 1.2), so
this experiment sets recursion_limit=25 to reach the safeguard quickly.

    python -m experiments.unbounded_retry
"""
from langgraph.graph import END, START, StateGraph

from app.nodes import fetch_context
from app.state import LookupState


def route_without_limit(state: LookupState) -> str:
    return "done" if state["success"] else "retry"


builder = StateGraph(LookupState)
builder.add_node("fetch_context", fetch_context)
builder.add_edge(START, "fetch_context")
builder.add_conditional_edges(
    "fetch_context",
    route_without_limit,
    {"done": END, "retry": "fetch_context"},
)
graph = builder.compile()

if __name__ == "__main__":
    print(graph.invoke(
        {"ticket": "my app keeps crashing", "attempts": 0,
         "available_after": 100},
        {"recursion_limit": 25},
    ))
