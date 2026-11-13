"""Scripted model for mechanical tests, not an observed provider response."""
import json
import re
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


class FixtureModel:
    def __init__(self):
        self.calls = 0

    def invoke(self, messages):
        self.calls += 1
        if isinstance(messages[-1], ToolMessage):
            data = json.loads(messages[-1].content)
            return AIMessage(content=(f"{data['ticket_id']}: {data['status']}; assigned to {data['assigned_to']}."
                                      if data["found"] else data["message"]))
        ticket = None
        for message in reversed(messages):
            if isinstance(message, HumanMessage):
                match = re.search(r"T-\d{4}", str(message.content))
                if match:
                    ticket = match.group(); break
        if not ticket:
            return AIMessage(content="Which ticket are you referring to?")
        return AIMessage(content="", tool_calls=[{"name":"get_ticket_status", "args":{"ticket_id":ticket},
                         "id":f"fixture_{self.calls}", "type":"tool_call"}])
