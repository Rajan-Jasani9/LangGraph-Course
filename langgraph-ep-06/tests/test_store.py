import unittest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from app.context import Context
from app.graph import build_graph
from app.tools import save_preference
from fixture_model import FixtureModel


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.store=InMemoryStore();self.model=FixtureModel();self.graph=build_graph(self.model,InMemorySaver(),self.store)
    def ask(self,user,thread,text):
        return self.graph.invoke({"messages":[("user",text)]},{"configurable":{"thread_id":thread},"recursion_limit":12},context=Context(user))
    def test_runtime_identity_is_not_model_argument(self):
        self.assertEqual(list(save_preference.tool_call_schema.model_json_schema()["properties"]),["preference"])
    def test_tool_writes_under_application_user(self):
        self.ask("user-1","a","Remember short updates.")
        self.assertEqual(self.store.get(("user-1","preferences"),"response_style").value,{"preference":"short updates."})
        self.assertIsNone(self.store.get(("user-2","preferences"),"response_style"))
    def test_new_thread_same_user_recalls(self):
        self.ask("user-1","a","Remember short updates.")
        self.assertIn("short updates",self.ask("user-1","b","My preference?")["messages"][-1].content)
    def test_other_user_does_not_inherit(self):
        self.ask("user-1","a","Remember short updates.")
        self.assertIn("No saved preference",self.ask("user-2","b","My preference?")["messages"][-1].content)
    def test_same_key_overwrites(self):
        self.ask("user-1","a","Remember short updates.");self.ask("user-1","b","Remember detailed updates.")
        self.assertEqual(self.store.get(("user-1","preferences"),"response_style").value["preference"],"detailed updates.")
    def test_injected_instruction_not_saved_as_message(self):
        self.ask("user-1","a","Remember short updates.");self.ask("user-1","b","My preference?")
        state=self.graph.get_state({"configurable":{"thread_id":"b"}}).values
        self.assertNotIn("system",[m.type for m in state["messages"]])
        self.assertIn("Saved response preference",self.model.inputs[-1][0].content)
    def test_new_store_is_empty(self):
        self.ask("user-1","a","Remember short updates.")
        self.assertIsNone(InMemoryStore().get(("user-1","preferences"),"response_style"))
    def test_delete_removes_future_lookup(self):
        self.ask("user-1","a","Remember short updates.");self.store.delete(("user-1","preferences"),"response_style")
        self.assertIn("No saved preference",self.ask("user-1","b","My preference?")["messages"][-1].content)


if __name__=="__main__":unittest.main()
