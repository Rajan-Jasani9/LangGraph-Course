from app.state import GreetingState


def clean_name(state: GreetingState) -> dict[str, str]:
    name = state["raw_name"].strip() or "friend"
    return {"name": name}


def greet(state: GreetingState) -> dict[str, str]:
    return {"greeting": f"Hello, {state['name']}!"}
