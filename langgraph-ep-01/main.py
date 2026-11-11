import argparse
import json

from app.graph import graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="  Rajan  ")
    parser.add_argument("--trace", action="store_true")
    args = parser.parse_args()
    initial = {"raw_name": args.name}

    if args.trace:
        for snapshot in graph.stream(initial, stream_mode="values"):
            print(json.dumps(snapshot))
    else:
        result = graph.invoke(initial)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
