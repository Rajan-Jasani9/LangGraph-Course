"""The first version from the video: fetch_context connects straight to END.

    python -m experiments.single_attempt
"""
import json

from langgraph.graph import END, START, StateGraph

from app.nodes import fetch_context
from app.state import LookupState

builder = StateGraph(LookupState)
builder.add_node("fetch_context", fetch_context)
builder.add_edge(START, "fetch_context")
builder.add_edge("fetch_context", END)
graph = builder.compile()

if __name__ == "__main__":
    initial = {"ticket": "my app keeps crashing", "attempts": 0,
               "available_after": 3}
    print(json.dumps(graph.invoke(initial), indent=2))
