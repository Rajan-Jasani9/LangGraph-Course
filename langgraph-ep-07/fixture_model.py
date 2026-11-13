import json
from langchain_core.messages import AIMessage,ToolMessage


class FixtureModel:
    """Scripted proposal, not a captured provider response."""
    def __init__(self):self.calls=0
    def invoke(self,messages):
        self.calls+=1
        if isinstance(messages[-1],ToolMessage):
            return AIMessage(content=messages[-1].content)
        return AIMessage(content="",tool_calls=[{"name":"change_ticket_priority","args":{"ticket_id":"T-1042","priority":"high"},"id":f"fixture_{self.calls}","type":"tool_call"}])
