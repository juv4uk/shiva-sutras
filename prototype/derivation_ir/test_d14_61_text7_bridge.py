#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import d14_61_text7_bridge as b
import test_savarna_dirgha_layers as layers


def corpus_result(a: str, c: str) -> str:
    for left, right, result in layers.ROWS:
        if (left, right) == (a, c):
            return result
    raise AssertionError(f"pair not present in pinned corpus: {(a, c)}")


class D14Text7BridgeTests(unittest.TestCase):
    def test_replays_merged_three_layer_witness_without_vidyut_authority(self):
        s = b.summary()
        self.assertEqual(s["specification"], ["1.1.9", "6.1.101"])
        self.assertEqual(s["vidyut_role"], "evidence-not-authority")
        self.assertEqual(s["layer1_rows"], 70)
        self.assertEqual(s["layer1_applications"], 16)
        self.assertGreater(s["layer2_annotated"], 0)
        self.assertGreater(s["layer3_annotated"], 0)
        self.assertFalse(s["corpus_first_position_o"])
        self.assertFalse(s["corpus_first_position_l_vocalic"])
        self.assertEqual(s["d14_coordinates_allocated"], 0)

    def test_positive_rule_application_is_typed_and_produces_text7_output(self):
        found = None
        for a, c, result in layers.ROWS:
            witness = b.classify(a, c, result)
            if witness.application.status == "ASSERTED-APPLICABLE":
                found = (a, c, result, witness)
                break
        self.assertIsNotNone(found)
        a, c, result, witness = found
        self.assertEqual(witness.application.relation, "applies-to")
        self.assertEqual(witness.application.required_classes, ("ak", "ac"))
        self.assertEqual(witness.transformation.relation, "produces")
        self.assertEqual(witness.transformation.output, result)
        self.assertEqual(witness.vidyut_relation, "AGREES-EVIDENCE")

        trace = b.build_positive_trace(a, c, result)
        self.assertEqual(trace["typed_application"]["status"], "ASSERTED-APPLICABLE")
        self.assertEqual(trace["typed_transformation"]["output"], result)
        self.assertEqual(trace["vidyut"]["role"], "AGREES-EVIDENCE")
        self.assertEqual(trace["proof_certificate"]["status"], "success")

    def test_e_plus_e_is_named_rule_scope_fact_not_geometry_failure(self):
        result = corpus_result("e", "e")
        witness = b.classify("e", "e", result)
        self.assertEqual(witness.layer, 3)
        self.assertEqual(witness.application.status, "ANNOTATED-RULE-SCOPE")
        self.assertEqual(witness.transformation.relation, "no-transition")
        self.assertIsNone(witness.transformation.output)

    def test_r_l_is_named_varttika_layer(self):
        result = corpus_result("ṛ", "ḷ")
        witness = b.classify("ṛ", "ḷ", result)
        self.assertEqual(witness.layer, 2)
        self.assertEqual(witness.application.status, "ANNOTATED-VARTTIKA")
        self.assertEqual(witness.vidyut_relation, "CLASSIFIED-DISAGREEMENT-WITH-VARTTIKA")

    def test_every_layer1_row_agrees_with_asserted_specification_and_evidence(self):
        checked = 0
        applied = 0
        for a, c, result in layers.ROWS:
            witness = b.classify(a, c, result)
            if witness.layer != 1:
                continue
            checked += 1
            self.assertEqual(witness.vidyut_relation, "AGREES-EVIDENCE")
            self.assertIn(
                witness.application.status,
                {"ASSERTED-APPLICABLE", "ASSERTED-NOT-APPLICABLE"},
            )
            if witness.application.status == "ASSERTED-APPLICABLE":
                applied += 1
                self.assertEqual(witness.transformation.output, result)
        self.assertEqual(checked, 70)
        self.assertEqual(applied, 16)


if __name__ == "__main__":
    unittest.main(verbosity=2)
