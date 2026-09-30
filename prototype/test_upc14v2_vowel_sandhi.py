#!/usr/bin/env python3
"""Vowel sandhi as graph queries: witnesses (shiva-sutras#44)."""

import csv
import os
import unittest

import upc14v2 as g
import upc14v2_vowel_sandhi as vs

HERE = os.path.dirname(__file__)
S = g.SOUNDS
L = g.LABELS_BY_CODE


class ClassTests(unittest.TestCase):
    def test_classes_are_computed_from_the_path(self):
        self.assertEqual({L[c] for c in vs.AC}, set("aiufxeoEO"))
        self.assertEqual({L[c] for c in vs.AK}, set("aiufx"))
        self.assertEqual({L[c] for c in vs.IK}, set("iufx"))
        self.assertEqual({L[c] for c in vs.EC}, set("eoEO"))
        self.assertEqual({L[c] for c in vs.YAN}, set("yvrl"))


class RuleTests(unittest.TestCase):
    def test_dirgha_6_1_101(self):
        for x, want in (("a", "A"), ("A", "A"), ("i", "I"), ("I", "I"), ("u", "U"), ("f", "F")):  # no ḷ + ḷ here
            self.assertEqual(vs.vowel_sandhi(x, x).text, want, x)
        self.assertEqual(vs.vowel_sandhi("a", "A").sounds, ("A",))

    def test_guna_and_rapara_6_1_87(self):
        self.assertEqual(vs.vowel_sandhi("a", "i").text, "e")
        self.assertEqual(vs.vowel_sandhi("A", "u").text, "o")
        r = vs.vowel_sandhi("a", "f")
        self.assertEqual((r.text, r.trace), ("ar", ("6.1.87", "1.1.51")))
        self.assertEqual(vs.vowel_sandhi("a", "x").text, "al")

    def test_vrddhi_6_1_88(self):
        for right, want in (("e", "E"), ("o", "O"), ("E", "E"), ("O", "O")):
            self.assertEqual(vs.vowel_sandhi("a", right).text, want, right)

    def test_yan_6_1_77_is_the_nearest_semivowel(self):
        for left, want in (("i", "y"), ("I", "y"), ("u", "v"), ("f", "r")):
            self.assertEqual(vs.vowel_sandhi(left, "a").text, want + "a", left)

    def test_ayavayav_6_1_78_decomposes_the_join(self):
        self.assertEqual(vs.vowel_sandhi("e", "i", padanta=False).text, "ayi")
        self.assertEqual({vs.decompose(S[x]) == (S[a], S[b]) for x, a, b in (("e", "a", "i"), ("o", "a", "u"))}, {True})
        first, second = vs.decompose(S["E"])
        self.assertEqual((L[second], g.unpack(first).length), ("i", g.LONG))   # ai = long a + i

    def test_the_apavadas_6_1_109_and_6_1_97(self):
        self.assertEqual(vs.vowel_sandhi("e", "a").trace, ("6.1.109",))      # agne 'tra
        self.assertEqual(vs.vowel_sandhi("o", "a").text, "o")                # vayo 'tra
        self.assertEqual(vs.vowel_sandhi("e", "A").text, "ayA")                # long ā is not `ati` (tapara)
        self.assertEqual(vs.vowel_sandhi("a", "e", padanta=False).text, "e")  # 6.1.97 pararupa
        self.assertEqual(vs.vowel_sandhi("a", "a", padanta=False).text, "a")
        self.assertEqual(vs.vowel_sandhi("a", "a", padanta=True).text, "A")   # at a boundary: 6.1.101
        self.assertEqual(vs.vowel_sandhi("a", "i", padanta=False).text, "e")  # 6.1.87 is untouched

    def test_no_rule_leaves_the_pair_alone(self):
        self.assertEqual(vs.vowel_sandhi("i", "u").text, "yu")                # 6.1.77 (u is not savarna with i)
        self.assertEqual(vs.vowel_sandhi("a", "a").trace, ("6.1.101",))


class VariantsAndBoundaryTests(unittest.TestCase):
    def test_a_va_rule_has_no_primary_result_only_variants(self):
        r = vs.vowel_sandhi("f", "f", vartika=True)
        self.assertEqual(set(r.variants), {("F",), ("f",)})          # hotṝkāraḥ / hotṛkāraḥ
        self.assertEqual(vs.vowel_sandhi("i", "a").variants, (("y", "a"),))   # an obligatory rule: one

    def test_the_kasika_examples_of_6_1_78_are_inside_a_word(self):
        self.assertEqual(vs.vowel_sandhi("e", "a").text, "e")                 # word-final e + a: 6.1.109
        self.assertEqual(vs.vowel_sandhi("e", "a", padanta=False).text, "aya")   # cayanam

    def test_6_1_97_blocks_vrddhi_as_well_as_dirgha(self):
        # pace (pac + e), yaje (yaj + e): inside a word a + e / o gives the following sound, not ai / au
        self.assertEqual(vs.vowel_sandhi("a", "e", padanta=False).text, "e")
        self.assertEqual(vs.vowel_sandhi("a", "e", padanta=True).text, "E")


class KasikaExampleTests(unittest.TestCase):
    """Examples the panini agent tabulated from the Kasika (second-hand: not re-read here)."""

    def test_the_examples(self):
        self.assertEqual(vs.vowel_sandhi("i", "a").text, "ya")                       # dadhy atra
        for left, right, want in (("e", "a", "aya"), ("o", "a", "ava"), ("E", "a", "Aya"), ("O", "a", "Ava")):
            self.assertEqual(vs.vowel_sandhi(left, right, padanta=False).text, want)  # cayanam lavanam cayakah lavakah


class AdhikaraTests(unittest.TestCase):
    def test_which_sutras_stand_under_6_1_84(self):
        for sutra in ("6.1.87", "6.1.88", "6.1.97", "6.1.101", "6.1.109", "6.1.111"):
            self.assertTrue(vs.under_ekadesa(sutra), sutra)
        for sutra in ("6.1.77", "6.1.78", "6.1.84", "6.1.112", "1.1.51", "8.4.40"):
            self.assertFalse(vs.under_ekadesa(sutra), sutra)

    def test_the_result_says_whether_the_pair_became_one_sound(self):
        for pair, want in ((("a", "i"), True), (("a", "e"), True), (("a", "a"), True), (("e", "a"), True),
                           (("i", "a"), False), (("E", "i"), False)):
            self.assertEqual(vs.vowel_sandhi(*pair).ekadesa, want, pair)


class VidyutTests(unittest.TestCase):
    """154 vowel + vowel rows of vidyut's generated external-sandhi rules."""

    @staticmethod
    def rows():
        path = os.path.join(HERE, "oracles", "vidyut-sandhi-vowels.tsv")
        with open(path, encoding="utf-8") as handle:
            lines = [line for line in handle if not line.startswith("#")]
        return list(csv.DictReader(lines, delimiter="\t"))

    def test_127_of_154_agree_and_the_other_27_are_only_the_optional_yv_elision(self):
        rows = self.rows()
        self.assertEqual(len(rows), 154)
        agree, elided = 0, []
        for row in rows:
            mine = vs.vowel_sandhi(row["first_slp1"], row["second_slp1"]).text
            theirs = row["result_slp1"].replace(" ", "").replace("'", "")
            if mine == theirs:
                agree += 1
            else:
                elided.append((row["first_slp1"], row["second_slp1"], mine.replace("y", "") == theirs))
        self.assertEqual(agree, 127)
        self.assertEqual(len(elided), 27)
        self.assertTrue(all(ok for _, _, ok in elided), elided)      # 8.3.19: y dropped after a / A
        self.assertEqual({first for first, _, _ in elided}, {"e", "E"})


class RVocalicTests(unittest.TestCase):
    """6.1.101 for ṛ and ḷ. Kasika, tabulated by the shiva agent: ḷ has no long form (line 389);
    'rti r va', 'lrti lr va': hotṝkāraḥ / hotṛkāraḥ, hotṝkāraḥ / hotlṛkāraḥ."""

    def test_the_vartika_gives_the_long_r_or_the_short_vowel_that_follows(self):
        for left, right in (("f", "f"), ("f", "x"), ("x", "x"), ("x", "f")):
            r = vs.vowel_sandhi(left, right, vartika=True)
            self.assertEqual(r.sounds, ("F",), (left, right))            # the dirgha variant
            self.assertEqual(r.options, ((right,),), (left, right))      # the va variant: the following vowel
            self.assertEqual(r.trace, ("6.1.101", "vartika"))

    def test_there_is_no_long_l(self):
        with self.assertRaises(g.GraphError):
            g.dirgha(S["x"], S["x"])
        for left, right in (("f", "f"), ("f", "x"), ("x", "x"), ("x", "f")):
            for vartika in (False, True):
                self.assertNotIn("X", vs.vowel_sandhi(left, right, vartika=vartika).text)

    def test_without_the_vartika_r_l_pairs_fall_to_yan_and_are_marked_unattested(self):
        for left, right, want in (("f", "x", "rx"), ("x", "f", "lf"), ("x", "x", "lx")):
            r = vs.vowel_sandhi(left, right)
            self.assertEqual((r.text, r.trace), (want, ("6.1.77",)))
            self.assertIn("not attested", r.note)
        r = vs.vowel_sandhi("f", "f")                                    # the sutra alone: long r
        self.assertEqual((r.text, r.note), ("F", ""))


class SavarnaVartikaTests(unittest.TestCase):
    def test_r_and_l_are_savarna_only_with_the_vartika(self):
        self.assertFalse(g.savarna(S["f"], S["x"]))                # 1.1.9 as written: places differ
        self.assertTrue(g.savarna(S["f"], S["x"], vartika=True))   # the Kasika's stipulation
        self.assertFalse(g.savarna(S["f"], S["r"], vartika=True))  # a vowel and r never (1.1.10)
        self.assertFalse(g.savarna(S["a"], S["i"], vartika=True))


class StartOccurrenceTests(unittest.TestCase):
    """Case `later-h-is-not-initial-h-for-hR` of panini/tests/pratyahara-exhaustive-v0.1.yaml."""

    def test_default_takes_the_first_recitation_as_the_tradition_does(self):
        self.assertEqual(len(g.start_ranks(S["h"])), 2)
        self.assertEqual({L[c] for c in g.pratyahara(S["h"], "R")}, set("hyvrl"))
        self.assertEqual(len(g.pratyahara(S["h"], "l")), 34)        # hal: h twice in the stream

    def test_strict_mode_refuses_to_guess(self):
        with self.assertRaises(g.AmbiguousStart):
            g.pratyahara(S["h"], "R", strict=True)
        with self.assertRaises(g.AmbiguousStart):
            g.pratyahara(S["h"], "l", strict=True)
        self.assertEqual(len(g.pratyahara(S["h"], "l", strict=True, start_occurrence=1)), 34)

    def test_the_second_h_has_no_R_after_it(self):
        with self.assertRaises(g.GraphError):
            g.pratyahara(S["h"], "R", start_occurrence=2)
        self.assertEqual(len(g.pratyahara(S["h"], "l", start_occurrence=2)), 1)   # just the last h


if __name__ == "__main__":
    unittest.main()
