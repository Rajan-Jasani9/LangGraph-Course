from app.state import TicketState


def route_ticket(state: TicketState) -> str:
    return state["category"]
