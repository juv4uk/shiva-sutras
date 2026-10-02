#!/usr/bin/env python3
import unittest

import upc7_geometry as geo
from upc7_sound import UPC7SoundError, project_sound, sound_table


class UPC7SoundProjectionTests(unittest.TestCase):
    def test_exact_seven_bit_identity_is_preserved(self):
        for profile in ("sa", "uk"):
            rows = sound_table(profile)
            self.assertEqual(128, len(rows))
            for code, row in enumerate(rows):
                self.assertEqual(code, row.code)
                self.assertEqual(f"{code:07b}", row.bits)

    def test_shared_k_has_profile_spellings_but_same_sound(self):
        code = geo.varga_code(0, 0)
        sa = project_sound(code, "sa")
        uk = project_sound(code, "uk")
        self.assertEqual("k", sa.spelling)
        self.assertEqual("к", uk.spelling)
        self.assertEqual("k", sa.ipa)
        self.assertEqual("k", uk.ipa)

    def test_sanskrit_h_and_ukrainian_g_are_distinct_cells(self):
        sa_h = project_sound(geo.nonvarga_code(5, 0), "sa")
        uk_h_cell = project_sound(geo.nonvarga_code(5, 1), "uk")
        self.assertEqual("h", sa_h.spelling)
        self.assertEqual("ɦ", sa_h.ipa)
        self.assertEqual("г", uk_h_cell.spelling)
        self.assertEqual("ɦ", uk_h_cell.ipa)
        self.assertNotEqual(sa_h.code, uk_h_cell.code)

    def test_profile_difference_is_not_hidden(self):
        r_code = geo.nonvarga_code(3, 2)
        sa = project_sound(r_code, "sa")
        uk = project_sound(r_code, "uk")
        self.assertEqual("unresolved", sa.status)
        self.assertIn("r", sa.ipa_candidates)
        self.assertEqual("resolved", uk.status)
        self.assertEqual("r", uk.ipa)

    def test_softness_is_context_modifier_not_standalone_phone(self):
        row = project_sound(geo.softness_code(), "uk")
        self.assertEqual("modifier", row.kind)
        self.assertEqual("context-required", row.status)
        self.assertIsNone(row.ipa)

    def test_sign_is_explicitly_non_sound(self):
        row = project_sound(geo.sign_code("space"), "uk")
        self.assertEqual("non-sound", row.kind)
        self.assertEqual("non-sound", row.status)

    def test_unassigned_cell_fails_closed(self):
        row = project_sound(0b0011001, "sa")
        self.assertEqual("unassigned", row.kind)
        self.assertEqual("unassigned", row.status)
        self.assertIsNone(row.ipa)

    def test_unknown_profile_rejected(self):
        with self.assertRaises(UPC7SoundError):
            project_sound(0, "xx")


if __name__ == "__main__":
    unittest.main()
