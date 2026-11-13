from langchain_core.tools import tool

from app.data import TICKETS


@tool
def get_ticket_status(ticket_id: str) -> dict:
    """Look up the current status and assignee of a support ticket by its ID."""
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return {"ticket_id": ticket_id, "found": False,
                "message": f"No ticket found for {ticket_id}"}
    return {"ticket_id": ticket_id, "found": True, **ticket}
