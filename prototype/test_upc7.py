#!/usr/bin/env python3
import unittest

from upc7 import UPC7, UPC7Error, UnrenderableCode


class UPC7Tests(unittest.TestCase):
    def setUp(self):
        self.u = UPC7()

    def test_current_upc8_assignment_fits_in_seven_bits(self):
        self.assertTrue(self.u.assigned_codes())
        self.assertLessEqual(max(self.u.assigned_codes()), 0x7F)

    def test_sanskrit_slp1_round_trip_preserves_codes(self):
        codes = self.u.encode("karma", "sa-slp1")
        self.assertEqual(self.u.render(codes, "sa-slp1"), "karma")
        self.assertEqual(self.u.encode(self.u.render(codes, "bits"), "bits"), codes)

    def test_ukrainian_multigraph_round_trip(self):
        codes = self.u.encode("джаз", "uk")
        self.assertEqual(self.u.render(codes, "uk"), "джаз")

    def test_layout_switch_preserves_identity(self):
        # k/i/m are explicit shared UPC-8 identities in both profiles.
        source_codes = self.u.encode("kim", "sa-slp1")
        self.assertEqual(self.u.render(source_codes, "uk"), "кім")
        self.assertEqual(self.u.encode("кім", "uk"), source_codes)
        self.assertTrue(self.u.preserves_codes_when_switching("kim", "sa-slp1", "uk"))

    def test_near_equivalence_is_not_silently_merged(self):
        # Sanskrit a is code 0x00; Ukrainian а is a separate near-equivalent
        # extension code 0x33. Layout switching must not pretend they are the
        # same identity.
        with self.assertRaises(UnrenderableCode):
            self.u.switch_layout("a", "sa-slp1", "uk")

    def test_bits_are_exactly_seven_wide(self):
        codes = self.u.encode("kim", "sa-slp1")
        diagnostic = self.u.render(codes, "bits")
        self.assertTrue(all(len(cell) == 7 for cell in diagnostic.split()))
        self.assertEqual(self.u.encode(diagnostic, "bits"), codes)

    def test_eight_bit_code_is_rejected(self):
        with self.assertRaises(UPC7Error):
            self.u.render([0x80], "bits")


if __name__ == "__main__":
    unittest.main()
