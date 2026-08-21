#!/usr/bin/env python3
"""
Comprehensive Test Suite for 64-Bit Pratyāhāra Bitmask Engine.
Run: python3 prototype/bitmask64/test_bitmask64.py
"""

import unittest
from bitmask64 import (
    CANONICAL_SOUNDS,
    SOUND_TO_BIT,
    BIT_TO_SOUND,
    PRATYAHARA_TABLE_64,
    sound_to_bit,
    is_member,
    get_pratyahara_mask,
    mask_intersect,
    mask_union,
    mask_diff,
    mask_subset,
    mask_disjoint,
    mask_count,
    mask_to_sounds,
    sounds_to_mask,
    export_c_header,
    export_verilog_lut,
)

class TestBitmask64(unittest.TestCase):

    def test_canonical_sound_space(self):
        """Verify sound space consists of exactly 42 unique canonical codes."""
        self.assertEqual(len(CANONICAL_SOUNDS), 42)
        self.assertEqual(len(SOUND_TO_BIT), 42)
        self.assertEqual(len(BIT_TO_SOUND), 42)
        self.assertEqual(SOUND_TO_BIT["a"], 0)
        self.assertEqual(SOUND_TO_BIT["s"], 41)

    def test_pratyahara_cardinalities(self):
        """Verify classical pratyāhāra cardinalities (popcounts)."""
        ac_mask = get_pratyahara_mask("ac")
        hal_mask = get_pratyahara_mask("hal")
        al_mask = get_pratyahara_mask("al")
        ik_mask = get_pratyahara_mask("ik")
        ec_mask = get_pratyahara_mask("ec")
        sar_mask = get_pratyahara_mask("Sar")
        yar_mask = get_pratyahara_mask("yaR")

        self.assertEqual(mask_count(ac_mask), 9)   # 9 vowels
        self.assertEqual(mask_count(hal_mask), 33) # 33 consonants (marker collision resolved)
        self.assertEqual(mask_count(al_mask), 42)  # 42 total sounds
        self.assertEqual(mask_count(ik_mask), 4)   # i, u, ṛ, ḷ
        self.assertEqual(mask_count(ec_mask), 4)   # e, o, ai, au
        self.assertEqual(mask_count(sar_mask), 3)  # ś, ṣ, s
        self.assertEqual(mask_count(yar_mask), 4)  # y, v, r, l

    def test_set_algebra_partition(self):
        """ac (vowels) and hal (consonants) form an exact partition of al (all sounds)."""
        ac = get_pratyahara_mask("ac")
        hal = get_pratyahara_mask("hal")
        al = get_pratyahara_mask("al")

        # Disjoint: ac ∩ hal = ∅
        self.assertTrue(mask_disjoint(ac, hal))
        self.assertEqual(mask_intersect(ac, hal), 0)

        # Union: ac ∪ hal = al
        self.assertEqual(mask_union(ac, hal), al)

        # Difference: al \ ac = hal and al \ hal = ac
        self.assertEqual(mask_diff(al, ac), hal)
        self.assertEqual(mask_diff(al, hal), ac)

    def test_subsets_and_inclusions(self):
        """Verify subset relationships in Pāṇinian ontology."""
        ac = get_pratyahara_mask("ac")
        ik = get_pratyahara_mask("ik")
        ec = get_pratyahara_mask("ec")
        hal = get_pratyahara_mask("hal")
        sar = get_pratyahara_mask("Sar")
        yar = get_pratyahara_mask("yaR")

        # ik ⊆ ac and ec ⊆ ac
        self.assertTrue(mask_subset(ik, ac))
        self.assertTrue(mask_subset(ec, ac))

        # Sar ⊆ hal and yaR ⊆ hal
        self.assertTrue(mask_subset(sar, hal))
        self.assertTrue(mask_subset(yar, hal))

        # ik and ec are disjoint
        self.assertTrue(mask_disjoint(ik, ec))

    def test_membership_fast_path(self):
        """Verify 1-cycle membership queries on individual sounds and codes."""
        ac = get_pratyahara_mask("ac")
        hal = get_pratyahara_mask("hal")
        sar = get_pratyahara_mask("Sar")

        # Vowels
        self.assertTrue(is_member("a", ac))
        self.assertTrue(is_member("i", ac))
        self.assertFalse(is_member("k", ac))
        self.assertFalse(is_member("h", ac))

        # Consonants
        self.assertTrue(is_member("k", hal))
        self.assertTrue(is_member("p", hal))
        self.assertTrue(is_member("h", hal))
        self.assertTrue(is_member("l", hal)) # Sutra 6 'l' present
        self.assertFalse(is_member("a", hal))

        # Sibilants (Sar)
        self.assertTrue(is_member("S", sar))
        self.assertTrue(is_member("z", sar))
        self.assertTrue(is_member("s", sar))
        self.assertFalse(is_member("k", sar))

        # Numeric codes
        self.assertTrue(is_member(0x00, ac)) # a
        self.assertTrue(is_member(0x25, hal)) # k

    def test_de_morgans_laws(self):
        """Verify De Morgan's laws on bitmasks: ~(A ∪ B) = ~A ∩ ~B."""
        ik = get_pratyahara_mask("ik")
        ec = get_pratyahara_mask("ec")
        al = get_pratyahara_mask("al")

        # In universe al:
        comp_union = mask_diff(al, mask_union(ik, ec))
        inter_comp = mask_intersect(mask_diff(al, ik), mask_diff(al, ec))
        self.assertEqual(comp_union, inter_comp)

    def test_code_generators(self):
        """Verify C header and Verilog module code generation."""
        c_hdr = export_c_header()
        verilog_mod = export_verilog_lut()

        self.assertIn("UPC8_MASK_AC", c_hdr)
        self.assertIn("UPC8_MASK_HAL", c_hdr)
        self.assertIn("UPC8_IS_MEMBER", c_hdr)
        self.assertIn("module pratyahara_lut", verilog_mod)
        self.assertIn("assign is_member = pratyahara_mask[sound_code];", verilog_mod)

if __name__ == "__main__":
    unittest.main()
