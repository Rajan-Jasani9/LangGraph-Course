import argparse
import json

from app.graph import graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticket", default="my app keeps crashing")
    parser.add_argument("--updates", action="store_true")
    args = parser.parse_args()
    initial = {"ticket": args.ticket}

    if args.updates:
        for update in graph.stream(initial, stream_mode="updates"):
            print(json.dumps(update))
    else:
        print(json.dumps(graph.invoke(initial), indent=2))


if __name__ == "__main__":
    main()
