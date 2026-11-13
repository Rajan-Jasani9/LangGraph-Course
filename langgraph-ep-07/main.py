import argparse
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command
from app.graph import TOOLS,build_graph
from app.model import make_model
from app.tools import TICKETS
from fixture_model import FixtureModel


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--fixture",action="store_true");args=p.parse_args()
    model=FixtureModel() if args.fixture else make_model(TOOLS)
    with SqliteSaver.from_conn_string("approvals.sqlite") as saver:
        graph=build_graph(model,saver)
        config={"configurable":{"thread_id":"approval-001"},"recursion_limit":12}
        result=graph.invoke({"messages":[("user","Change T-1042 to high priority.")]},config)
        while result.get("__interrupt__"):
            print("Review:",result["__interrupt__"][0].value)
            print("Current ticket:",TICKETS["T-1042"])
            # Local reviewer input; a service must authenticate and authorize its reviewer.
            approved=input("Approve? [yes/no] ").strip().lower()=="yes"
            result=graph.invoke(Command(resume=approved),config)
        print(result["messages"][-1].content)
