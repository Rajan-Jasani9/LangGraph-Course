import json
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from app.context import Context
from app.graph import build_graph
from fixture_model import FixtureModel


def capture():
    store=InMemoryStore();model=FixtureModel();graph=build_graph(model,InMemorySaver(),store)
    def ask(user,thread,text):
        result=graph.invoke({"messages":[("user",text)]},{"configurable":{"thread_id":thread},"recursion_limit":12},context=Context(user))
        return result["messages"][-1].content
    saved=ask("user-1","a","Remember short updates and include the assigned team.")
    cross=ask("user-1","b","What's my preferred format?")
    other=ask("user-2","c","What's my preferred format?")
    updated=ask("user-1","d","Remember detailed updates with current status and assigned team.")
    recalled=ask("user-1","e","What's my preferred format?")
    record=store.get(("user-1","preferences"),"response_style").value
    state=graph.get_state({"configurable":{"thread_id":"b"}}).values
    return {"provenance":"Scripted model fixture; real ToolRuntime, InMemoryStore and LangGraph execution",
            "saved":saved,"new_thread_same_user":cross,"other_user":other,"updated":updated,"recall_updated":recalled,
            "stored_value":record,"new_store":InMemoryStore().get(("user-1","preferences"),"response_style"),
            "saved_state_types":[m.type for m in state["messages"]],
            "tool_schema_fields":list(__import__('app.tools',fromlist=['save_preference']).save_preference.tool_call_schema.model_json_schema()['properties'])}


if __name__=="__main__":print(json.dumps(capture(),indent=2))
