import os

from app.tools import get_ticket_status


def make_model(tools=None):
    from langchain_groq import ChatGroq

    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError("Set GROQ_API_KEY in your environment before a live run.")
    model = ChatGroq(
        model=os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b"),
        temperature=0,
        timeout=30,
        max_retries=1,
    )
    return model.bind_tools(tools if tools is not None else [get_ticket_status])
