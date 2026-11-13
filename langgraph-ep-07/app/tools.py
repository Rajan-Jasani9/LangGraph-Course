from typing import Literal
from langchain_core.tools import tool
from langgraph.types import interrupt

TICKETS = {"T-1042":{"status":"in progress","assigned_to":"backend team","priority":"medium"}}


@tool
def get_ticket_status(ticket_id: str) -> dict:
    """Read the current status, assignee and priority of a local support ticket."""
    return {"ticket_id":ticket_id,**TICKETS[ticket_id]} if ticket_id in TICKETS else {"found":False,"ticket_id":ticket_id}


@tool
def change_ticket_priority(ticket_id: str, priority: Literal["low","medium","high"]) -> dict:
    """Propose a priority change. A human decision is required before the write."""
    if ticket_id not in TICKETS:
        return {"changed":False,"reason":"ticket not found"}
    if priority not in {"low","medium","high"}:
        raise ValueError("Invalid priority")
    approved = interrupt({"ticket_id":ticket_id,"requested_priority":priority,
                          "message":"Approve this priority change?"})
    if approved is not True:
        return {"changed":False,"reason":"cancelled by reviewer","priority":TICKETS[ticket_id]["priority"]}
    # Node code before interrupt may replay. Mutations belong after approval.
    TICKETS[ticket_id]["priority"] = priority
    return {"changed":True,"ticket_id":ticket_id,"priority":priority}
