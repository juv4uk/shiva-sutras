#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import d14_61_pratyahara_operands as d


class OperandEdgeTests(unittest.TestCase):
    def test_6_1_77_aci_resolves_to_existing_ac_node(self):
        edge = d.edge_for("6.1.77", "aci", node_id="opaque:A")
        self.assertEqual(edge.relation, "uses-class")
        self.assertEqual(edge.canonical_class, "ac")
        self.assertEqual(edge.grammatical_form, "locative-singular")
        self.assertEqual(
            set(edge.class_node.members),
            {"a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au"},
        )

    def test_6_1_101_akah_resolves_to_existing_ak_node(self):
        edge = d.edge_for("6.1.101", "akaḥ", node_id="opaque:B")
        self.assertEqual(edge.relation, "uses-class")
        self.assertEqual(edge.canonical_class, "ak")
        self.assertEqual(edge.grammatical_form, "genitive-singular")
        self.assertEqual(set(edge.class_node.members), {"a", "i", "u", "ṛ", "ḷ"})

    def test_6_1_101_inherits_aci_context_without_new_class_table(self):
        inherited = d.edge_for("6.1.101", "aci", node_id="opaque:A")
        direct = d.edge_for("6.1.77", "aci", node_id="opaque:A")
        self.assertEqual(inherited.relation, "inherits-class-context")
        self.assertEqual(inherited.class_node, direct.class_node)

    def test_opaque_node_relabel_does_not_change_semantics(self):
        edge = d.edge_for("6.1.101", "akaḥ", node_id="opaque:before")
        moved = d.relabel(edge, "opaque:after")
        self.assertNotEqual(edge.class_node.node_id, moved.class_node.node_id)
        self.assertEqual(edge.class_node.canonical_name, moved.class_node.canonical_name)
        self.assertEqual(edge.class_node.members, moved.class_node.members)
        self.assertEqual(edge.relation, moved.relation)
        self.assertEqual(edge.provenance, moved.provenance)

    def test_unresolved_source_form_fails_closed(self):
        with self.assertRaises(KeyError):
            d.edge_for("6.1.101", "hal")

    def test_unknown_pratyahara_fails_closed(self):
        with self.assertRaises(Exception):
            d.resolve_pratyahara("not-a-pratyahara")

    def test_bounded_map_allocates_no_d14_coordinate(self):
        for edge in d.bounded_edges():
            self.assertFalse(hasattr(edge.class_node, "d14_coordinate"))
            self.assertEqual(edge.evidence_tier, "repo-grounded-control")
            self.assertTrue(edge.provenance)


if __name__ == "__main__":
    unittest.main(verbosity=2)
