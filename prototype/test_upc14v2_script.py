#!/usr/bin/env python3
"""IAST, Devanagari and Cyrillic views of the 42 sounds (stage 1 of removing SLP1)."""

import itertools
import random
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


def _alphabet():
    return (list(S.values()) + [g.e_long(S[k]) for k in "aiuf"] + [g.e_nasal(S[k]) for k in "aiufxeoEO"]
            + [g.e_nasal(g.e_long(S[k])) for k in "aiuf"])


class TextCodecTests(unittest.TestCase):
    """A sequence of sounds -> a string -> the same sequence, in every script, no ambiguity."""

    SCRIPTS = ("iast", "devanagari", "cyrillic")

    def test_every_pair_round_trips_and_no_two_sequences_share_a_string(self):
        alphabet = _alphabet()
        for script in self.SCRIPTS:
            seen = {}
            for n in (1, 2):
                for seq in itertools.product(alphabet, repeat=n):
                    text = sc.encode_text(seq, script)
                    self.assertEqual(sc.decode_text(text, script), seq, (script, text))
                    self.assertNotIn(text, seen, (script, text))     # injective
                    seen[text] = seq

    def test_random_longer_sequences_round_trip(self):
        rng = random.Random(14)
        alphabet = _alphabet()
        for script in self.SCRIPTS:
            for _ in range(4000):
                seq = tuple(rng.choice(alphabet) for _ in range(rng.randint(3, 7)))
                self.assertEqual(sc.decode_text(sc.encode_text(seq, script), script), seq, script)

    def test_the_ambiguous_junctions_get_a_dot_in_iast_and_cyrillic(self):
        k, h, kh, a, i, ai, y = (S[x] for x in ("k", "h", "K", "a", "i", "E", "y"))
        self.assertEqual(sc.encode_text([k, h], "iast"), "k·h")
        self.assertEqual(sc.encode_text([kh], "iast"), "kh")
        self.assertEqual(sc.encode_text([a, i], "iast"), "a·i")
        self.assertEqual(sc.encode_text([ai], "iast"), "ai")
        self.assertEqual(sc.encode_text([a, y], "cyrillic"), "а·й")
        self.assertEqual(sc.encode_text([ai], "cyrillic"), "ай")
        self.assertEqual(sc.decode_text("kh", "iast"), (kh,))
        self.assertEqual(sc.decode_text("k·h", "iast"), (k, h))

    def test_no_dot_where_the_text_is_already_unambiguous(self):
        self.assertEqual(sc.encode_text([S["k"], S["t"], S["a"]], "iast"), "kta")

    def test_devanagari_follows_the_writing_system(self):
        k, a, R = S["k"], S["a"], S["R"]
        long_a = g.e_long(a)
        self.assertEqual(sc.encode_text([k, a], "devanagari"), "क")           # k + inherent a
        self.assertEqual(sc.encode_text([k], "devanagari"), "क्")
        self.assertEqual(sc.encode_text([k, S["i"]], "devanagari"), "कि")     # a vowel sign
        self.assertEqual(sc.encode_text([k, a, R, long_a], "devanagari"), "कणा")
        self.assertEqual(sc.encode_text([k, a, a], "devanagari"), "कअ")       # hiatus: independent letter

    def test_transcode_goes_through_the_codes(self):
        text = sc.encode_text([S["k"], S["R"], S["a"], g.e_long(S["a"])], "iast")
        for src in self.SCRIPTS:
            for dst in self.SCRIPTS:
                s = sc.transcode(sc.transcode(text, "iast", src), src, dst)
                self.assertEqual(sc.decode_text(s, dst), sc.decode_text(text, "iast"))

    def test_a_string_that_is_not_a_text_of_the_script_raises(self):
        for script, bad in (("iast", "kq"), ("cyrillic", "z"), ("devanagari", "k")):
            with self.assertRaises(g.GraphError):
                sc.decode_text(bad, script)


if __name__ == "__main__":
    unittest.main()
