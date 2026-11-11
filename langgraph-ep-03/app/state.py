from typing import TypedDict, NotRequired


class LookupState(TypedDict):
    ticket: str
    attempts: int
    success: NotRequired[bool]
    result: NotRequired[str]
    available_after: int
