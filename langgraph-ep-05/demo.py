"""Actual LangGraph checkpoint operations with a clearly identified model fixture."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from langgraph.checkpoint.memory import InMemorySaver
from app.graph import build_graph
from fixture_model import FixtureModel


def config(thread):
    return {"configurable":{"thread_id":thread}, "recursion_limit":12}


def conversation(graph, thread, text):
    result=graph.invoke({"messages":[("user",text)]},config(thread))
    return {"answer":result["messages"][-1].content,"message_count":len(result["messages"])}


def capture():
    graph=build_graph(FixtureModel(),InMemorySaver())
    first=conversation(graph,"support-chat-001","Status of T-1042?")
    follow=conversation(graph,"support-chat-001","Who's handling it?")
    empty=conversation(graph,"support-chat-002","Who's handling it?")
    second=conversation(graph,"support-chat-002","Status of T-2008?")
    switch=conversation(graph,"support-chat-001","Who's handling it?")
    snapshot=graph.get_state(config("support-chat-001"))
    fresh=conversation(build_graph(FixtureModel(),InMemorySaver()),"support-chat-001","Who's handling it?")
    with tempfile.TemporaryDirectory() as temp:
        database=str(Path(temp)/"checkpoints.sqlite")
        def process(text):
            return json.loads(subprocess.check_output([sys.executable,"-B","main.py",text,"--fixture","--database",database],text=True,cwd=Path(__file__).parent))
        sqlite_first=process("Status of T-1042?")
        sqlite_after_restart=process("Is that ticket resolved yet?")
    return {"provenance":"Scripted model fixture; actual LangGraph checkpointers and separate Python processes",
            "first":first,"follow":follow,"new_thread":empty,"second_ticket":second,"switch_back":switch,
            "snapshot_types":[m.type for m in snapshot.values["messages"]],"fresh_ram":fresh,
            "sqlite_first":sqlite_first,"sqlite_after_restart":sqlite_after_restart}


if __name__=="__main__":print(json.dumps(capture(),indent=2))
