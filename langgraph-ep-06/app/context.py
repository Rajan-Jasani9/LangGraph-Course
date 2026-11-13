from dataclasses import dataclass


@dataclass(frozen=True)
class Context:
    # The application supplies identity after authentication; never take it from model arguments.
    user_id: str
