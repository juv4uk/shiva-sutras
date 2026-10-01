#!/usr/bin/env python3
"""UPC-7 cells derived from the UPC-14 graph, against the hand-placed table (hypothesis)."""

import unittest

import upc14v2 as g
import upc14v2_sandhi as sd
import upc7_derive as d
import upc7_geometry as geo

S = g.SOUNDS


class DerivedCellsTests(unittest.TestCase):
    def test_43_of_46_cells_equal_the_hand_placed_ones(self):
        agree, differ, missing = d.compare()
        self.assertEqual((len(agree), len(differ), len(missing)), (43, 3, 0))
        self.assertEqual({name for name, _, _ in differ}, {"r", "l", "h"})

    def test_the_three_differences_are_exactly_these(self):
        # r: the graph puts it with ṛ ṭ ṣ (retroflex, Kasika), the hand table with s l (dental).
        # l: the hand table gives it a `lateral` slot of its own; the graph tells r from l by place.
        # h: the graph has it throat + voiced (gh lifted, Panini: kanthya, ghosa); the hand table has a
        #    glottal place and a voiceless slot (IPA-like).
        _, differ, _ = d.compare()
        got = {name: (format(derived, "07b"), format(hand, "07b")) for name, derived, hand in differ}
        self.assertEqual(got, {"r": ("0101010", "0101110"), "l": ("0101110", "0101111"),
                               "h": ("0100001", "0110100")})

    def test_the_derived_cells_are_injective_on_the_sounds(self):
        names = list(S) + ["ā", "ī", "ū", "ṝ"]
        cells = [d.derive(sd.code_of(n)) for n in names]
        self.assertEqual(len(set(cells)), len(cells))

    def test_the_derived_class_is_the_geometry_class(self):
        for name in S:
            cell = d.derive(S[name])
            ap = g.unpack(S[name]).aperture
            expected = {g.STOP: geo.CLASS_VARGA, g.SEMIVOWEL: geo.CLASS_NONVARGA, g.SIBILANT: geo.CLASS_NONVARGA,
                        g.VOWEL: geo.CLASS_VOWEL, g.WIDE_VOWEL: geo.CLASS_VOWEL}[ap]
            self.assertEqual(geo.class_of(cell), expected, name)

    def test_varga_cells_decode_to_the_place_and_member_of_the_graph(self):
        rows = (("k", "kh", "g", "gh", "ṅ"), ("c", "ch", "j", "jh", "ñ"), ("ṭ", "ṭh", "ḍ", "ḍh", "ṇ"),
                ("t", "th", "d", "dh", "n"), ("p", "ph", "b", "bh", "m"))
        for place, row in enumerate(rows):
            for member, name in enumerate(row):
                self.assertEqual(geo.decode_varga(d.derive(S[name])), (place, member), name)

    def test_vowel_cells_carry_row_nasal_and_length(self):
        for name, row, long_ in (("a", 0, False), ("ā", 0, True), ("i", 1, False), ("ī", 1, True), ("u", 2, False),
                                 ("ū", 2, True), ("ṛ", 3, False), ("ṝ", 3, True), ("ḷ", 4, False),
                                 ("e", 5, False), ("ai", 5, True), ("o", 6, False), ("au", 6, True)):
            self.assertEqual(geo.decode_vowel(d.derive(sd.code_of(name))), (row, False, long_), name)

    def test_nasal_vowels_are_the_same_rows_with_the_nose(self):
        for name, row in (("a", 0), ("i", 1), ("u", 2), ("ṛ", 3), ("ḷ", 4)):
            code = g.e_nasal(S[name])
            self.assertEqual(geo.decode_vowel(d.derive(code)), (row, True, False), name)

    def test_a_vertex_without_a_vowel_row_is_refused(self):
        weird = g.Vertex(g.K | g.M, 0, g.VOWEL, 0, 1, 0).code
        with self.assertRaises(d.DeriveError):
            d.derive(weird)


if __name__ == "__main__":
    unittest.main()
