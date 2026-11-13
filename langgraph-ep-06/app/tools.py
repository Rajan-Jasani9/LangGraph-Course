from langchain_core.tools import tool

from app.data import TICKETS
from langgraph.prebuilt import ToolRuntime
from app.context import Context


@tool
def save_preference(preference: str, runtime: ToolRuntime[Context]) -> dict:
    """Save or update the user's ticket-response style only when explicitly requested."""
    user_id = runtime.context.user_id
    if not user_id or not preference.strip() or len(preference) > 500:
        raise ValueError("A valid application identity and a nonempty preference up to 500 characters are required.")
    namespace = (user_id, "preferences")
    runtime.store.put(namespace, "response_style", {"preference": preference.strip()})
    return {"saved": True, "key": "response_style"}


@tool
def get_ticket_status(ticket_id: str) -> dict:
    """Look up the current status and assignee of a support ticket by its ID."""
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return {"ticket_id": ticket_id, "found": False,
                "message": f"No ticket found for {ticket_id}"}
    return {"ticket_id": ticket_id, "found": True, **ticket}
