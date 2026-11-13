import argparse
import json

from app.graph import build_graph
from app.model import make_model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?", default="What's the status of ticket T-1042?")
    parser.add_argument("--updates", action="store_true")
    parser.add_argument("--inspect", action="store_true", help="Call the bound model only; no tools execute")
    args = parser.parse_args()
    model = make_model()
    if args.inspect:
        message = model.invoke([("user", args.question)])
        print(json.dumps({"content": message.content, "tool_calls": message.tool_calls}, indent=2))
        return
    graph = build_graph(model)
    initial = {"messages": [("user", args.question)]}
    # An execution guard, not a guarantee of task success or safe side effects.
    config = {"recursion_limit": 12}
    if args.updates:
        for update in graph.stream(initial, config=config, stream_mode="updates"):
            for node, patch in update.items():
                for message in patch["messages"]:
                    print(json.dumps({"node": node, "type": message.type,
                                      "content": message.content,
                                      "tool_calls": getattr(message, "tool_calls", []),
                                      "tool_call_id": getattr(message, "tool_call_id", None)}))
    else:
        result = graph.invoke(initial, config=config)
        print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
