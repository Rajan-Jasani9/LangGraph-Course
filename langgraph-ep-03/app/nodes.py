from app.state import LookupState


def fetch_context(state: LookupState) -> dict:
    attempt = state["attempts"] + 1
    if attempt < state["available_after"]:
        return {"attempts": attempt, "success": False}
    return {
        "attempts": attempt,
        "success": True,
        "result": "Ticket context retrieved.",
    }


def escalate_ticket(state: LookupState) -> dict:
    return {
        "result": "Support service unreachable. "
        "Ticket needs manual review."
    }
