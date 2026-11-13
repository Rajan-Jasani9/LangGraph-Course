"""Scripted model fixture. This is not evidence of live model instruction-following."""
import json
import re
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


class FixtureModel:
    def __init__(self):self.inputs=[]
    def invoke(self, messages):
        self.inputs.append(messages)
        if isinstance(messages[-1],ToolMessage):
            data=json.loads(messages[-1].content)
            if data.get("saved"):return AIMessage(content="Your response preference was saved.")
            return AIMessage(content=f"{data['ticket_id']}: {data.get('status','not found')}; {data.get('assigned_to','no matching ticket')}.")
        text=str(next(m.content for m in reversed(messages) if isinstance(m,HumanMessage)))
        if text.lower().startswith("remember"):
            return AIMessage(content="",tool_calls=[{"name":"save_preference","args":{"preference":text[len('remember'):].strip()},"id":f"fixture_{len(self.inputs)}","type":"tool_call"}])
        match=re.search(r"T-\d{4}",text)
        if match:
            return AIMessage(content="",tool_calls=[{"name":"get_ticket_status","args":{"ticket_id":match.group()},"id":f"fixture_{len(self.inputs)}","type":"tool_call"}])
        marker="Saved response preference (user data): "
        instruction=str(messages[0].content)
        return AIMessage(content=instruction.split(marker,1)[1] if marker in instruction else "No saved preference for this user.")
