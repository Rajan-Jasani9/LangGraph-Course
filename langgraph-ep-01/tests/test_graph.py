import unittest

from app.graph import graph
from app.nodes import clean_name


class GraphTests(unittest.TestCase):
    def test_whitespace_and_preserved_input(self):
        result = graph.invoke({"raw_name": "  Rajan  "})
        self.assertEqual(result, {
            "raw_name": "  Rajan  ", "name": "Rajan",
            "greeting": "Hello, Rajan!",
        })

    def test_blank_name_fallback(self):
        self.assertEqual(graph.invoke({"raw_name": "   "})["greeting"],
                         "Hello, friend!")

    def test_trace_has_three_snapshots(self):
        snapshots = list(graph.stream({"raw_name": "  Mira  "},
                                    stream_mode="values"))
        self.assertEqual(snapshots, [
            {"raw_name": "  Mira  "},
            {"raw_name": "  Mira  ", "name": "Mira"},
            {"raw_name": "  Mira  ", "name": "Mira",
             "greeting": "Hello, Mira!"},
        ])

    def test_node_patch_preserves_input(self):
        before = {"raw_name": "  Rajan  "}
        self.assertEqual(clean_name(before), {"name": "Rajan"})
        self.assertEqual(before, {"raw_name": "  Rajan  "})

    def test_missing_input_raises(self):
        with self.assertRaises(KeyError):
            graph.invoke({})

    def test_independent_invocations(self):
        graph.invoke({"raw_name": "Rajan"})
        self.assertEqual(graph.invoke({"raw_name": "Mira"})["greeting"],
                         "Hello, Mira!")


if __name__ == "__main__":
    unittest.main()
