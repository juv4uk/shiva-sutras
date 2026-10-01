#!/usr/bin/env python3
"""IAST, Devanagari and Cyrillic views of the 42 sounds (stage 1 of removing SLP1)."""

import unicodedata

import unittest

import upc14v2 as g
import upc14v2_script as sc

S = g.SOUNDS


class ScriptViewTests(unittest.TestCase):
    def test_every_sound_round_trips_in_both_scripts(self):
        for key, code in S.items():
            with self.subTest(sound=key):
                self.assertEqual(sc.code_from_iast(sc.to_iast(code)), code)
                self.assertEqual(sc.code_from_devanagari(sc.to_devanagari(code)), code)

    def test_the_42_spellings_are_distinct_in_each_script(self):
        self.assertEqual(len({sc.to_iast(c) for c in S.values()}), 42)
        self.assertEqual(len({sc.to_devanagari(c) for c in S.values()}), 42)

    def test_iast_has_no_capital_letters(self):
        for code in S.values():
            self.assertEqual(sc.to_iast(code), sc.to_iast(code).lower())

    def test_devanagari_is_devanagari_only(self):
        for code in S.values():
            self.assertTrue(all("ऀ" <= ch <= "ॿ" for ch in sc.to_devanagari(code)))

    def test_long_and_nasal_vowels_are_spelled_by_rule(self):
        spelled = {key: (sc.to_iast(g.e_long(S[key])), sc.to_devanagari(g.e_long(S[key]))) for key in "aiuf"}
        self.assertEqual(spelled, {"a": ("ā", "आ"), "i": ("ī", "ई"), "u": ("ū", "ऊ"), "f": ("ṝ", "ॠ")})
        self.assertEqual(sc.to_devanagari(g.e_nasal(S["a"])), "अँ")
        self.assertEqual(sc.code_from_iast("ā"), g.e_long(S["a"]))
        self.assertEqual(sc.code_from_iast("ã"), g.e_nasal(S["a"]))

    def test_known_spellings(self):
        for iast, dev, key in (("kh", "ख्", "K"), ("ṇ", "ण्", "R"), ("ś", "श्", "S"), ("ai", "ऐ", "E"), ("ṛ", "ऋ", "f")):
            self.assertEqual(sc.code_from_iast(iast), S[key])
            self.assertEqual(sc.code_from_devanagari(dev), S[key])

    def test_a_spelling_that_is_not_a_sound_raises(self):
        for bad in ("K", "x", "", "kk"):
            with self.assertRaises(g.GraphError):
                sc.code_from_iast(bad)


class CyrillicViewTests(unittest.TestCase):
    """The Cyrillic table is a hypothesis (Vaishnava practice from memory); these tests pin its form."""

    def test_every_sound_round_trips_and_the_42_are_distinct(self):
        for key, code in S.items():
            with self.subTest(sound=key):
                self.assertEqual(sc.code_from_cyrillic(sc.to_cyrillic(code)), code)
        self.assertEqual(len({sc.to_cyrillic(c) for c in S.values()}), 42)

    def test_only_cyrillic_letters_and_combining_marks(self):
        for code in S.values():
            for ch in sc.to_cyrillic(code):
                self.assertTrue("\u0400" <= ch <= "\u04ff" or unicodedata.combining(ch), (ch, hex(ord(ch))))

    def test_known_spellings(self):
        for cyr, key in (("кх", "K"), ("т\u0323", "w"), ("н\u0323", "R"), ("ш\u0301", "S"), ("ай", "E"), ("дж", "j"), ("й", "y")):
            self.assertEqual(sc.code_from_cyrillic(cyr), S[key])

    def test_long_and_nasal_vowels(self):
        self.assertEqual(sc.to_cyrillic(g.e_long(S["a"])), "а\u0304")
        self.assertEqual(sc.to_cyrillic(g.e_long(S["u"])), "\u04ef")   # NFC: у + macron composes
        self.assertEqual(sc.code_from_cyrillic("а\u0303"), g.e_nasal(S["a"]))

    def test_the_three_scripts_name_the_same_42_sounds(self):
        for code in S.values():
            self.assertEqual(sc.code_from_iast(sc.to_iast(code)), sc.code_from_cyrillic(sc.to_cyrillic(code)))


if __name__ == "__main__":
    unittest.main()
