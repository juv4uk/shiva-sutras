#!/usr/bin/env python3
import unittest

import akshara7 as a7
import trishula14 as t14

class Akshara7Tests(unittest.TestCase):
    def test_inventory_and_round_trip(self):
        self.assertEqual(len(a7.SOUND_CODE), 42)
        for sound, code in a7.SOUND_CODE.items():
            self.assertEqual(a7.decode(code), sound)
            self.assertEqual(a7.parse_bits(a7.bits(code)), (code,))

    def test_reserved_and_eight_bit_cells_fail_closed(self):
        with self.assertRaises(a7.InvalidCode):
            a7.check(0b1100000)
        with self.assertRaises(a7.InvalidCode):
            a7.check(0b0000000 + 42)
        with self.assertRaises(a7.InvalidCode):
            a7.parse_bits("10000000")

    def test_pratyahara_excludes_marker(self):
        self.assertEqual([a7.decode(x) for x in a7.pratyahara("a", "ṇ")], ["a", "i", "u"])

class Trishula14Tests(unittest.TestCase):
    def test_inventory_is_distinct_and_fourteen_wide(self):
        self.assertEqual(len(t14.FEATURES), 42)
        codes = [t14.encode(s) for s in t14.FEATURES]
        self.assertEqual(len(set(codes)), 42)
        self.assertTrue(all(len(t14.bits(c)) == 14 for c in codes))

    def test_feature_fields_are_decodable(self):
        for sound in ("k", "gh", "a", "ai", "ś", "h"):
            self.assertEqual(t14.decode(t14.encode(sound)), sound)

    def test_unassigned_but_well_shaped_code_is_rejected(self):
        # Same field shape as a stop, but a stop member outside the canonical set.
        with self.assertRaises(t14.InvalidCode):
            t14.check(t14.Feature(t14.KIND_STOP, 0, 7).code)
        with self.assertRaises(t14.InvalidCode):
            t14.check(1 << 13)

    def test_pratyahara_excludes_marker(self):
        self.assertEqual([t14.decode(x) for x in t14.pratyahara("a", "ṇ")], ["a", "i", "u"])

if __name__ == "__main__":
    unittest.main()
