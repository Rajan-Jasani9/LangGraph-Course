import unittest

from app.graph import graph
from app.nodes import classify_ticket
from app.routing import route_ticket
from experiments.missing_route import graph as graph_without_fallback


def nodes_that_ran(ticket):
    updates = graph.stream({"ticket": ticket}, stream_mode="updates")
    return [node for update in updates for node in update]


class RoutingTests(unittest.TestCase):
    def test_technical_ticket(self):
        result = graph.invoke({"ticket": "my app keeps crashing"})
        self.assertEqual(result["category"], "technical")
        self.assertEqual(result["response"], "Please share your error logs.")

    def test_billing_ticket(self):
        result = graph.invoke({"ticket": "I was charged twice"})
        self.assertEqual(result["category"], "billing")
        self.assertEqual(result["response"],
                         "Please provide your transaction details.")

    def test_unknown_ticket_reaches_fallback(self):
        result = graph.invoke({"ticket": "hello"})
        self.assertEqual(result["category"], "unknown")
        self.assertIn("more information", result["response"])

    def test_keyword_check_ignores_case(self):
        self.assertEqual(classify_ticket({"ticket": "APP CRASHED"}),
                         {"category": "technical"})

    def test_first_matching_condition_wins(self):
        ticket = "the invoice page shows an error"
        self.assertEqual(classify_ticket({"ticket": ticket}),
                         {"category": "technical"})

    def test_router_returns_a_label_not_a_state_update(self):
        self.assertEqual(route_ticket({"ticket": "x", "category": "billing"}),
                         "billing")

    def test_only_the_selected_path_runs(self):
        self.assertEqual(nodes_that_ran("I was charged twice"),
                         ["classify", "billing_help"])
        self.assertEqual(nodes_that_ran("my app keeps crashing"),
                         ["classify", "technical_help"])
        self.assertEqual(nodes_that_ran("hello"), ["classify", "fallback"])

    def test_unmapped_label_is_an_error(self):
        with self.assertRaises(KeyError) as caught:
            graph_without_fallback.invoke({"ticket": "hello"})
        self.assertEqual(caught.exception.args[0], "unknown")


if __name__ == "__main__":
    unittest.main()
