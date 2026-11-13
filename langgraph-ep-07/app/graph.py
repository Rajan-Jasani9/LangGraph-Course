from langchain_core.messages import SystemMessage
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from app.tools import change_ticket_priority, get_ticket_status

TOOLS=[get_ticket_status,change_ticket_priority]


def build_graph(model,checkpointer):
    def call_model(state:MessagesState):
        response=model.invoke([SystemMessage(content="Use the registered tools for ticket facts and requested changes. Never claim a change before tool confirmation."),*state["messages"]])
        return {"messages":[response]}
    builder=StateGraph(MessagesState)
    builder.add_node("agent",call_model)
    builder.add_node("tools",ToolNode(TOOLS))
    builder.add_edge(START,"agent")
    builder.add_conditional_edges("agent",tools_condition)
    builder.add_edge("tools","agent")
    return builder.compile(checkpointer=checkpointer)
