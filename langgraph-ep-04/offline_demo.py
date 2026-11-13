"""Deterministic model fixture; actual LangGraph and ToolNode execution, no API.

This verifies graph mechanics. It is NOT evidence of Groq model behavior.
"""
import json
import importlib.metadata

from langchain_core.messages import AIMessage, ToolMessage

from app.graph import build_graph


class FixtureModel:
    def __init__(self, ticket_id=None):
        self.ticket_id = ticket_id
        self.inputs = []

    def invoke(self, messages):
        self.inputs.append(messages)
        last = messages[-1] if messages else None
        if isinstance(last, ToolMessage):
            data = json.loads(last.content)
            text = (f"Ticket {data['ticket_id']} is {data['status']} and assigned to the {data['assigned_to']}."
                    if data["found"] else data["message"])
            return AIMessage(content=text)
        if self.ticket_id:
            return AIMessage(content="", tool_calls=[{
                "name": "get_ticket_status", "args": {"ticket_id": self.ticket_id},
                "id": "fixture_call_1", "type": "tool_call",
            }])
        return AIMessage(content="Ticket priority describes how urgently a support issue should be handled.")


def run(ticket_id, question):
    model = FixtureModel(ticket_id)
    graph = build_graph(model)
    trace = []
    for update in graph.stream({"messages": [("user", question)]},
                               config={"recursion_limit": 12}, stream_mode="updates"):
        for node, patch in update.items():
            for m in patch["messages"]:
                trace.append({"node": node, "type": m.type, "content": m.content,
                              "tool_calls": getattr(m, "tool_calls", []),
                              "tool_call_id": getattr(m, "tool_call_id", None)})
    return {"trace": trace, "model_calls": len(model.inputs)}


if __name__ == "__main__":
    print(json.dumps({"provenance": "Scripted model fixture; real LangGraph/ToolNode; no live provider call",
                      "versions": {p: importlib.metadata.version(p) for p in
                                   ["langgraph", "langchain-core", "langchain-groq"]},
                      "known": run("T-1042", "What's the status of ticket T-1042?"),
                      "general": run(None, "What does ticket priority mean?"),
                      "missing": run("T-9999", "What's the status of ticket T-9999?")}, indent=2))
