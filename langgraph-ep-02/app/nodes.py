from app.state import TicketState


def classify_ticket(state: TicketState) -> dict[str, str]:
    text = state["ticket"].lower()
    if "crash" in text or "error" in text or "bug" in text:
        category = "technical"
    elif "charged" in text or "refund" in text or "invoice" in text:
        category = "billing"
    else:
        category = "unknown"
    return {"category": category}


def technical_help(state: TicketState) -> dict[str, str]:
    return {"response": "Please share your error logs."}


def billing_help(state: TicketState) -> dict[str, str]:
    return {"response": "Please provide your transaction details."}


def fallback(state: TicketState) -> dict[str, str]:
    return {
        "response": "Could you provide a little more "
        "information about your issue?"
    }
