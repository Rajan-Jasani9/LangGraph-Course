import unittest
from langgraph.checkpoint.memory import InMemorySaver
from app.graph import build_graph
from fixture_model import FixtureModel
from demo import config, conversation, capture


class MemoryTests(unittest.TestCase):
    def setUp(self):self.graph=build_graph(FixtureModel(),InMemorySaver())
    def test_same_thread_retains_context(self):
        conversation(self.graph,"a","Status of T-1042?")
        self.assertIn("backend team",conversation(self.graph,"a","Who's handling it?")["answer"])
    def test_new_thread_does_not_inherit(self):
        conversation(self.graph,"a","Status of T-1042?")
        self.assertIn("Which ticket",conversation(self.graph,"b","Who's handling it?")["answer"])
    def test_threads_keep_respective_tickets(self):
        conversation(self.graph,"a","Status of T-1042?");conversation(self.graph,"b","Status of T-2008?")
        self.assertIn("T-1042",conversation(self.graph,"a","Follow up?")["answer"])
        self.assertIn("T-2008",conversation(self.graph,"b","Follow up?")["answer"])
    def test_snapshot_contains_tool_pair(self):
        conversation(self.graph,"a","Status of T-1042?")
        self.assertEqual([m.type for m in self.graph.get_state(config("a")).values["messages"]],["human","ai","tool","ai"])
    def test_fresh_memory_saver_is_empty(self):
        conversation(self.graph,"a","Status of T-1042?")
        fresh=build_graph(FixtureModel(),InMemorySaver())
        self.assertEqual(fresh.get_state(config("a")).values,{})
    def test_no_checkpointer_means_no_cross_invocation_history(self):
        graph=build_graph(FixtureModel())
        graph.invoke({"messages":[("user","T-1042?")]})
        self.assertIn("Which ticket",graph.invoke({"messages":[("user","Who's handling it?")]})["messages"][-1].content)
    def test_sqlite_recovers_in_a_new_python_process(self):
        result=capture()
        self.assertIn("T-1042",result["sqlite_after_restart"]["answer"])
        self.assertGreater(len(result["sqlite_after_restart"]["messages"]),len(result["sqlite_first"]["messages"]))


if __name__=="__main__":unittest.main()
