from app.state import LookupState


def route_after_fetch(state: LookupState) -> str:
    if state["success"]:
        return "done"
    if state["attempts"] >= 3:
        return "escalate"
    return "retry"
