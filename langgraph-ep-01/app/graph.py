from langgraph.graph import END, START, StateGraph

from app.nodes import clean_name, greet
from app.state import GreetingState


builder = StateGraph(GreetingState)
builder.add_node("clean_name", clean_name)
builder.add_node("greet", greet)

builder.add_edge(START, "clean_name")
builder.add_edge("clean_name", "greet")
builder.add_edge("greet", END)

graph = builder.compile()
