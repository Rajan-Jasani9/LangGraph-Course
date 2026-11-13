import json
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from app.graph import build_graph
from app.tools import TICKETS
from fixture_model import FixtureModel


def capture():
    TICKETS["T-1042"]["priority"]="medium"
    graph=build_graph(FixtureModel(),InMemorySaver())
    config={"configurable":{"thread_id":"approval-001"},"recursion_limit":12}
    request={"messages":[("user","Change T-1042 to high priority.")]}
    paused=graph.invoke(request,config)
    before=TICKETS["T-1042"]["priority"]
    rejected=graph.invoke(Command(resume=False),config)
    after_reject=TICKETS["T-1042"]["priority"]
    again=graph.invoke(request,config)
    approved=graph.invoke(Command(resume=True),config)
    return {"provenance":"Scripted model proposal; actual ToolNode interrupt and Command resume; local dictionary only",
            "interrupt_payload":paused["__interrupt__"][0].value,"priority_while_paused":before,
            "reject_result":json.loads(rejected["messages"][-1].content),"priority_after_reject":after_reject,
            "second_request_paused":bool(again.get("__interrupt__")),
            "approve_result":json.loads(approved["messages"][-1].content),"priority_after_approve":TICKETS["T-1042"]["priority"]}


if __name__=="__main__":print(json.dumps(capture(),indent=2))
