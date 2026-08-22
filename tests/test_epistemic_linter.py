#!/usr/bin/env python3
"""Unittest wrapper: the epistemic linter runs as part of the test suite,
so a violation of the methodological contract is red exactly like a code
regression."""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import epistemic_linter  # noqa: E402


class EpistemicLinterTests(unittest.TestCase):
    def setUp(self):
        self.result = epistemic_linter.run_lint()

    def test_no_violations(self):
        self.assertEqual(
            [],
            [f"{rule}: {msg}" for rule, msg in self.result.violations],
            "epistemic contract violated - see details above",
        )

    def test_preregistration_is_still_blind(self):
        """R5's most important property while L-001 has not run."""
        import yaml
        doc = yaml.safe_load(open(epistemic_linter.PREREG_DOC, encoding="utf-8"))
        self.assertEqual("", str(doc.get("outcome_class", "")).strip(),
                         "outcome_class must stay empty until the run completes")
        self.assertIsNone(doc.get("run_started_at"),
                          "run_started_at set means the preregistration "
                          "window is closed; changes now require a new "
                          "revision + journal entry")

    def test_invalidated_datasets_are_declared(self):
        self.assertGreaterEqual(
            len(epistemic_linter.invalidated_datasets(
                open(epistemic_linter.FREEZE_DOC, encoding="utf-8").read())),
            1,
            "the invalidation list must not be emptied silently")


if __name__ == "__main__":
    unittest.main()
