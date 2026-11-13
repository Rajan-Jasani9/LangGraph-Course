import argparse
import json
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

from app.graph import build_graph
from app.model import make_model
from fixture_model import FixtureModel


def run(args, saver):
    graph = build_graph(FixtureModel() if args.fixture else make_model(), saver)
    config = {"configurable": {"thread_id": args.thread}, "recursion_limit": 12}
    if not args.inspect:
        graph.invoke({"messages": [("user", args.question)]}, config)
    snapshot = graph.get_state(config)
    messages = snapshot.values.get("messages", [])
    print(json.dumps({"thread": args.thread, "messages": [
        {"type":m.type, "content":m.content, "tool_calls":getattr(m,"tool_calls",[])} for m in messages
    ], "answer": messages[-1].content if messages else None}))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("question", nargs="?", default="What's the status of ticket T-1042?")
    p.add_argument("--thread", default="support-chat-001")
    p.add_argument("--backend", choices=["memory","sqlite"], default="sqlite")
    p.add_argument("--database", default="checkpoints.sqlite")
    p.add_argument("--fixture", action="store_true")
    p.add_argument("--inspect", action="store_true")
    args = p.parse_args()
    if args.backend == "sqlite":
        with SqliteSaver.from_conn_string(args.database) as saver:
            run(args, saver)
    else:
        run(args, InMemorySaver())
