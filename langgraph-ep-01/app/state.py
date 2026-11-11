from typing import NotRequired, TypedDict


class GreetingState(TypedDict):
    raw_name: str
    name: NotRequired[str]
    greeting: NotRequired[str]
