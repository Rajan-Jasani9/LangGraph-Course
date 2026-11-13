import unittest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from app.graph import build_graph
from app.tools import TICKETS,change_ticket_priority
from fixture_model import FixtureModel


class ApprovalTests(unittest.TestCase):
    def setUp(self):
        TICKETS["T-1042"]["priority"]="medium";self.graph=build_graph(FixtureModel(),InMemorySaver());self.config={"configurable":{"thread_id":"test"},"recursion_limit":12}
    def pause(self):return self.graph.invoke({"messages":[("user","Change T-1042 to high.")]},self.config)
    def test_pauses_before_mutation(self):
        result=self.pause();self.assertTrue(result["__interrupt__"]);self.assertEqual(TICKETS["T-1042"]["priority"],"medium")
    def test_payload_matches_proposal(self):
        self.assertEqual(self.pause()["__interrupt__"][0].value["requested_priority"],"high")
    def test_reject_keeps_medium(self):
        self.pause();self.graph.invoke(Command(resume=False),self.config);self.assertEqual(TICKETS["T-1042"]["priority"],"medium")
    def test_approve_changes_to_high(self):
        self.pause();self.graph.invoke(Command(resume=True),self.config);self.assertEqual(TICKETS["T-1042"]["priority"],"high")
    def test_string_true_is_not_approval(self):
        self.pause();self.graph.invoke(Command(resume="true"),self.config);self.assertEqual(TICKETS["T-1042"]["priority"],"medium")
    def test_every_new_request_requires_approval(self):
        self.pause();self.graph.invoke(Command(resume=False),self.config);self.assertTrue(self.pause()["__interrupt__"])
    def test_schema_restricts_priorities(self):
        schema=change_ticket_priority.args_schema.model_json_schema();self.assertEqual(schema["properties"]["priority"]["enum"],["low","medium","high"])


if __name__=="__main__":unittest.main()
