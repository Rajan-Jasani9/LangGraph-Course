import argparse
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from app.context import Context
from app.graph import TOOLS, build_graph
from app.model import make_model
from fixture_model import FixtureModel


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--fixture",action="store_true")
    p.add_argument("--user",default="user-1",help="Controlled local test identity; a backend must authenticate this")
    args=p.parse_args()
    store=InMemoryStore()
    model=FixtureModel() if args.fixture else make_model(TOOLS)
    graph=build_graph(model,InMemorySaver(),store)
    for thread,text in [("chat-001","Remember short ticket updates and include the assigned team."),
                        ("chat-002","What's my preferred format for ticket updates?"),
                        ("chat-002","What's the status of T-1042?")]:
        result=graph.invoke({"messages":[("user",text)]},
            {"configurable":{"thread_id":thread},"recursion_limit":12},context=Context(args.user))
        print(thread,result["messages"][-1].content)
    item=store.get((args.user,"preferences"),"response_style")
    print("Saved memory:",item.value if item else None)
