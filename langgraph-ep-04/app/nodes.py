from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState

SYSTEM = (
    "Use get_ticket_status for a specific ticket's current status or assignee. "
    "Only report ticket facts returned by the tool; never invent a status. "
    "If the tool says not found, say so. Answer general questions directly."
)


def make_call_model(model, system=SYSTEM):
    def call_model(state: MessagesState):
        response = model.invoke([
            SystemMessage(content=system),
            *state["messages"],
        ])
        return {"messages": [response]}

    return call_model
