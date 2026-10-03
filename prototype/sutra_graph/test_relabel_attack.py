#!/usr/bin/env python3
"""Synthetic fail-closed tests for #103 relabel_attack.py.

The fixture is intentionally invented. It validates graph invariance mechanics,
not Pāṇinian factual correctness.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    "relabel_attack",
    os.path.join(HERE, "relabel_attack.py"),
)
M = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


class RelabelAttackTests(unittest.TestCase):
    def setUp(self):
        self.edges = (
            M.Edge("rule-a", "rule-root", "adhikara", "scope-x"),
            M.Edge("rule-b", "rule-a", "anuvrtti", "term-y"),
            M.Edge("rule-c", "rule-a", "apavada", "explicit-ref"),
            M.Edge("rule-c", "rule-b", "kasika_ref", "apavada"),
        )

    def test_lawful_bijection_preserves_query(self):
        mapping = {
            "rule-a": "rule-c",
            "rule-b": "rule-root",
            "rule-c": "rule-a",
            "rule-root": "rule-b",
        }
        self.assertTrue(
            M.lawful_rename_invariant(
                self.edges,
                "rule-b",
                "anuvrtti",
                mapping,
                "term-y",
            )
        )

    def test_broken_rename_changes_query(self):
        mapping = {
            "rule-a": "rule-c",
            "rule-b": "rule-root",
            "rule-c": "rule-a",
            "rule-root": "rule-b",
        }
        self.assertTrue(
            M.broken_renaming_fails(
                self.edges,
                "rule-b",
                "anuvrtti",
                mapping,
                "term-y",
            )
        )

    def test_delete_required_edge_fails(self):
        self.assertTrue(
            M.delete_one_required_edge_fails(
                self.edges, "rule-b", "anuvrtti", "term-y"
            )
        )

    def test_wrong_edge_kind_fails(self):
        self.assertTrue(
            M.mutate_edge_kind_fails(
                self.edges, "rule-b", "anuvrtti", "term-y"
            )
        )

    def test_non_bijection_is_rejected(self):
        mapping = {
            "rule-a": "rule-a",
            "rule-b": "rule-a",
            "rule-c": "rule-c",
            "rule-root": "rule-root",
        }
        with self.assertRaises(ValueError):
            M.rename_graph(self.edges, mapping)

    def test_bounded_runner_has_zero_d14_allocation(self):
        result = M.run(self.edges, 32)
        self.assertEqual(result["lawful_relabel_passes"], 32)
        self.assertGreater(result["broken_relabel_changes"], 0)
        self.assertEqual(result["d14_forced_coordinates"], 0)


if __name__ == "__main__":
    unittest.main()
