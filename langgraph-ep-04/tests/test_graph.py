import json
import unittest

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.errors import GraphRecursionError
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, MessagesState, START, END

from app.graph import build_graph
from app.tools import get_ticket_status
from offline_demo import FixtureModel, run


def execute_tool(request):
    builder = StateGraph(MessagesState)
    builder.add_node("tools", ToolNode([get_ticket_status]))
    builder.add_edge(START, "tools")
    builder.add_edge("tools", END)
    return builder.compile().invoke({"messages": [request]})["messages"][-1]


class GraphTests(unittest.TestCase):
    def test_known_ticket(self):
        result = get_ticket_status.invoke({"ticket_id": "T-1042"})
        self.assertTrue(result["found"])
        self.assertEqual(result["assigned_to"], "backend team")

    def test_unknown_ticket(self):
        self.assertFalse(get_ticket_status.invoke({"ticket_id": "T-9999"})["found"])

    def test_tool_schema(self):
        schema = get_ticket_status.args_schema.model_json_schema()
        self.assertEqual(schema["properties"]["ticket_id"]["type"], "string")
        self.assertEqual(schema["required"], ["ticket_id"])

    def test_bound_request_does_not_execute(self):
        model = FixtureModel("T-1042")
        message = model.invoke([HumanMessage(content="status?")])
        self.assertEqual(message.tool_calls[0]["args"], {"ticket_id": "T-1042"})
        self.assertEqual(len(model.inputs), 1)
        self.assertFalse(any(isinstance(m, ToolMessage) for m in model.inputs[0]))

    def test_tool_result_pairing(self):
        request = AIMessage(content="", tool_calls=[{"name": "get_ticket_status",
                            "args": {"ticket_id": "T-1042"}, "id": "call_test", "type": "tool_call"}])
        message = execute_tool(request)
        self.assertEqual(message.tool_call_id, "call_test")
        self.assertTrue(json.loads(message.content)["found"])

    def test_conditional_routes(self):
        requested = FixtureModel("T-1042").invoke([])
        self.assertEqual(tools_condition({"messages": [requested]}), "tools")
        self.assertEqual(tools_condition({"messages": [AIMessage(content="hello")]}), "__end__")

    def test_complete_loop_and_history(self):
        model = FixtureModel("T-1042")
        result = build_graph(model).invoke({"messages": [("user", "status?")]})
        self.assertEqual([m.type for m in result["messages"]], ["human", "ai", "tool", "ai"])
        self.assertEqual([m.type for m in model.inputs[1]], ["system", "human", "ai", "tool"])

    def test_general_bypasses_tools(self):
        result = run(None, "priority?")
        self.assertEqual([m["node"] for m in result["trace"]], ["agent"])

    def test_missing_ticket_returns_normally(self):
        result = run("T-9999", "status?")
        self.assertEqual(result["model_calls"], 2)
        self.assertIn("No ticket found", result["trace"][-1]["content"])

    def test_unknown_tool_is_not_executed(self):
        request = AIMessage(content="", tool_calls=[{"name": "delete_record", "args": {},
                            "id": "bad", "type": "tool_call"}])
        result = execute_tool(request)
        self.assertEqual(result.status, "error")

    def test_nonterminating_model_hits_guard(self):
        class NeverAnswers:
            def invoke(self, messages):
                return FixtureModel("T-1042").invoke([])
        with self.assertRaises(GraphRecursionError):
            build_graph(NeverAnswers()).invoke({"messages": [("user", "status?")]},
                                               config={"recursion_limit": 4})

    def test_separate_invocations_do_not_remember(self):
        model = FixtureModel(None)
        graph = build_graph(model)
        graph.invoke({"messages": [("user", "T-1042?")]})
        graph.invoke({"messages": [("user", "Who is handling it?")]})
        self.assertEqual(len(model.inputs[-1]), 2)  # system + current question


if __name__ == "__main__":
    unittest.main()
