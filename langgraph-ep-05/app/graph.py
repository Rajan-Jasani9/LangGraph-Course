from langchain_core.messages import SystemMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.tools import get_ticket_status

SYSTEM = "Use get_ticket_status for ticket facts. Use conversation context to resolve follow-ups. Ask which ticket if context is missing. Never invent ticket facts."


def build_graph(model, checkpointer=None):
    def call_model(state: MessagesState):
        response = model.invoke([SystemMessage(content=SYSTEM), *state["messages"]])
        return {"messages": [response]}

    builder = StateGraph(MessagesState)
    builder.add_node("agent", call_model)
    builder.add_node("tools", ToolNode([get_ticket_status]))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    return builder.compile(checkpointer=checkpointer)
