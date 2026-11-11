import unittest

from langgraph.errors import GraphRecursionError

from app.graph import graph
from app.routing import route_after_fetch
from experiments.single_attempt import graph as single_attempt_graph
from experiments.unbounded_retry import graph as unbounded_graph


def initial(available_after):
    return {"ticket": "my app keeps crashing", "attempts": 0,
            "available_after": available_after}


def nodes_that_ran(available_after):
    updates = graph.stream(initial(available_after), stream_mode="updates")
    return [node for update in updates for node in update]


class RetryTests(unittest.TestCase):
    def test_succeeds_on_first_attempt(self):
        result = graph.invoke(initial(1))
        self.assertEqual(result["attempts"], 1)
        self.assertTrue(result["success"])

    def test_succeeds_on_the_last_allowed_attempt(self):
        result = graph.invoke(initial(3))
        self.assertEqual(result["attempts"], 3)
        self.assertTrue(result["success"])
        self.assertEqual(result["result"], "Ticket context retrieved.")

    def test_cycle_runs_the_same_node_again(self):
        self.assertEqual(nodes_that_ran(3), ["fetch_context"] * 3)

    def test_gives_up_and_escalates(self):
        self.assertEqual(nodes_that_ran(100),
                         ["fetch_context"] * 3 + ["escalate_ticket"])
        result = graph.invoke(initial(100))
        self.assertEqual(result["attempts"], 3)
        self.assertFalse(result["success"])
        self.assertIn("manual review", result["result"])

    def test_success_is_checked_before_the_limit(self):
        state = {**initial(3), "attempts": 3, "success": True}
        self.assertEqual(route_after_fetch(state), "done")

    def test_router_labels(self):
        base = initial(100)
        self.assertEqual(route_after_fetch(
            {**base, "attempts": 1, "success": False}), "retry")
        self.assertEqual(route_after_fetch(
            {**base, "attempts": 3, "success": False}), "escalate")

    def test_without_a_cycle_it_tries_once(self):
        result = single_attempt_graph.invoke(initial(3))
        self.assertEqual(result["attempts"], 1)
        self.assertFalse(result["success"])

    def test_unbounded_cycle_hits_the_recursion_limit(self):
        with self.assertRaises(GraphRecursionError):
            unbounded_graph.invoke(initial(100), {"recursion_limit": 25})


if __name__ == "__main__":
    unittest.main()
