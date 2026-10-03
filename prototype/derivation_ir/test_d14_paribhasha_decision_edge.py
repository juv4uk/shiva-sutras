#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import d14_paribhasha_decision_edge as d
from paribhasha_resolver import ParibhashaResolver
import upc14v2_vowel_sandhi as vs


class D14ParibhashaDecisionTests(unittest.TestCase):
    def test_kasika_source_attests_apavada_relation(self):
        self.assertTrue(d.kasika_attests_apavada())

    def test_real_word_final_e_a_conflict_emits_typed_decision(self):
        edge = d.decide("e", "a", padanta=True)
        self.assertIsNotNone(edge)
        self.assertEqual(edge.relation, "governs-rule-decision")
        self.assertEqual(edge.principle, "apavada")
        self.assertEqual(edge.selected_rule, "6.1.109")
        self.assertEqual(edge.rejected_rule, "6.1.78")
        self.assertEqual(edge.evidence_tier, "commentarial-supported")
        self.assertEqual(edge.source_id, "KASIKA-6.1.109")
        self.assertIn("padanta", edge.context)
        self.assertEqual(vs.vowel_sandhi("e", "a").trace, ("6.1.109",))

    def test_rule_order_does_not_change_apavada_decision(self):
        resolver = ParibhashaResolver()
        forward = resolver.resolve_binary_conflict(d.GENERAL, d.SPECIAL)
        reverse = resolver.resolve_binary_conflict(d.SPECIAL, d.GENERAL)
        for result in (forward, reverse):
            self.assertEqual(result.selected_rule.sutra_id, "6.1.109")
            self.assertEqual(result.rejected_rule.sutra_id, "6.1.78")
            self.assertEqual(result.winning_principle, "apavada")

    def test_internal_e_a_has_no_special_rule_conflict(self):
        self.assertIsNone(d.decide("e", "a", padanta=False))
        result = vs.vowel_sandhi("e", "a", padanta=False)
        self.assertEqual(result.trace, ("6.1.78",))
        self.assertEqual(result.text, "aya")

    def test_removing_apavada_fact_changes_the_proof_even_if_output_rule_stays_later(self):
        control = d.falsifier_without_apavada_fact()
        # 6.1.109 is still later in the text, so a naive output-only test would
        # miss the lost grammatical fact.  The proof relation must not.
        self.assertEqual(control.selected_rule.sutra_id, "6.1.109")
        self.assertEqual(control.winning_principle, "para")
        self.assertNotEqual(control.winning_principle, "apavada")

    def test_no_d14_coordinate_is_part_of_the_decision(self):
        edge = d.decide("o", "a", padanta=True)
        self.assertIsNotNone(edge)
        self.assertFalse(hasattr(edge, "d14_coordinate"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
