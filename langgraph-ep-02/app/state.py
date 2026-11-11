from typing import TypedDict, NotRequired


class TicketState(TypedDict):
    ticket: str
    category: NotRequired[str]
    response: NotRequired[str]
