#!/usr/bin/env python3
"""
Test Suite for Slavic & Ukrainian Phonetics Prototype.
Run: python3 prototype/slavic_phonetics/test_slavic_phonetics.py
"""

import unittest
from slavic_phonetics import (
    SLAVIC_REGISTRY,
    HARD_TO_SOFT,
    decompose_iotated,
    apply_first_palatalization,
    apply_second_palatalization,
    geometric_palatalization_shift,
)

class TestSlavicPhonetics(unittest.TestCase):

    def test_registry_completeness(self):
        """Verify feature matrix coverage for Ukrainian phoneme set."""
        self.assertIn("а", SLAVIC_REGISTRY)
        self.assertIn("дж", SLAVIC_REGISTRY)
        self.assertIn("ць", SLAVIC_REGISTRY)
        self.assertEqual(SLAVIC_REGISTRY["дж"].code, 0x38)
        self.assertEqual(SLAVIC_REGISTRY["ць"].code, 0x46)
        self.assertEqual(SLAVIC_REGISTRY["і"].soft, 1)

    def test_iotated_initial_and_postvocalic(self):
        """Word-initial, post-vocalic, and post-apostrophe decomposition."""
        # Initial яблуко -> [й, а, б, л, у, к, о]
        self.assertEqual(decompose_iotated("яблуко"), ["й", "а", "б", "л", "у", "к", "о"])

        # Post-vocalic маяк -> [м, а, й, а, к]
        self.assertEqual(decompose_iotated("маяк"), ["м", "а", "й", "а", "к"])

        # Post-apostrophe м'ясо -> [м, й, а, с, о]
        self.assertEqual(decompose_iotated("м'ясо"), ["м", "й", "а", "с", "о"])

        # 'ї' is always [й, і]: їжак -> [й, і, ж, а, к], поїзд -> [п, о, й, і, з, д]
        self.assertEqual(decompose_iotated("їжак"), ["й", "і", "ж", "а", "к"])
        self.assertEqual(decompose_iotated("поїзд"), ["п", "о", "й", "і", "з", "д"])

    def test_iotated_postconsonantal_softening(self):
        """Post-consonantal softening: дядько -> [дь, а, дь, к, о], людина -> [ль, у, д, и, н, а]."""
        self.assertEqual(decompose_iotated("дядько"), ["дь", "а", "дь", "к", "о"])
        self.assertEqual(decompose_iotated("людина"), ["ль", "у", "д", "и", "н", "а"])
        self.assertEqual(decompose_iotated("синє"), ["с", "и", "нь", "е"])

    def test_affricate_and_shch_parsing(self):
        """щ -> [ш, ч], дж, дз parsing."""
        # щит -> [ш, ч, и, т]
        self.assertEqual(decompose_iotated("щит"), ["ш", "ч", "и", "т"])
        # джаз -> [дж, а, з]
        self.assertEqual(decompose_iotated("джаз"), ["дж", "а", "з"])

    def test_first_palatalization_rules(self):
        """First Palatalization: к->ч (рука -> ручка), г->ж (нога -> ніжка), х->ш (муха -> мушка)."""
        self.assertEqual(apply_first_palatalization("к"), "ч")
        self.assertEqual(apply_first_palatalization("г"), "ж")
        self.assertEqual(apply_first_palatalization("х"), "ш")

    def test_second_palatalization_rules(self):
        """Second Palatalization: к->ць (рука -> руці), г->зь (нога -> нозі), х->сь (муха -> мусі)."""
        self.assertEqual(apply_second_palatalization("к"), "ць")
        self.assertEqual(apply_second_palatalization("г"), "зь")
        self.assertEqual(apply_second_palatalization("х"), "сь")

    def test_geometric_feature_shift(self):
        """Geometric displacement from Velar (4) to Postalveolar (2) / Dental (1)."""
        k_feat = SLAVIC_REGISTRY["к"]
        ch_feat = geometric_palatalization_shift(k_feat, rule=1)
        self.assertEqual(ch_feat.symbol, "ч")
        self.assertEqual(ch_feat.place, 2) # Postalveolar

        c_soft = geometric_palatalization_shift(k_feat, rule=2)
        self.assertEqual(c_soft.symbol, "ць")
        self.assertEqual(c_soft.place, 1) # Dental
        self.assertEqual(c_soft.soft, 1)  # Soft

if __name__ == "__main__":
    unittest.main()
