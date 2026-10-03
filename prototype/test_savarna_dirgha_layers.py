#!/usr/bin/env python3
"""savarṇa-dīrgha as an executable witness, in three explicit layers (Text7 candidate D).

The oracle is vidyut-sandhi-vowels.tsv (pinned by sha256 in docs/text7-candidate-d-ratification-2026-10-03.md).
Its OWN behaviour is the label: a junction is "dīrgha" iff vidyut merges the two vowels into one long vowel.

  LAYER 1  sūtra 1.1.9 + 6.1.101  : strict savarṇa. The bit predicate AND the bit mutation must reproduce vidyut
                                    exactly. This layer is ASSERTED.
  LAYER 2  vārttika (ṛ~ḷ)         : 1.1.9 alone does not give it; the vārttika does. vidyut does NOT merge ṛ+ḷ
                                    (r|ḷ). Text7 geometry (different rows) agrees with 1.1.9 and with vidyut. The
                                    disagreement is between vidyut and the vārttika, not with Text7. ANNOTATED.
  LAYER 3  wide-vowel step e~ai, o~au : one length bit cannot separate guṇa from vṛddhi; the bit predicate says
                                    "same row", 1.1.9 as implemented says "different aperture", vidyut does not merge.
                                    A documented precision limit (#2494). ANNOTATED, expressed by D14 context.

Rows with ḹ are skipped (Kāśikā: no such sound; D has no cell for it).
"""
from __future__ import annotations

import csv
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import upc14v2 as g
import upc14v2_sandhi as sd
import upc7_derive as d

CELLS = {n: d.derive(sd.code_of(n)) for n in list(g.SOUNDS) + ["ā", "ī", "ū", "ṝ"]}
NAME_OF = {c: n for n, c in CELLS.items()}
VOWEL, ROW_SHIFT = 0b10, 2
LONG_BIT = 1


def row(c): return (c & 31) >> 2
def is_vowel(c): return (c >> 5) == VOWEL


def bit_savarna(a: int, b: int) -> bool:
    return is_vowel(a) and is_vowel(b) and row(a) == row(b)


def bit_dirgha(a: int, b: int):
    """6.1.101 on bits: same row -> that row, long, oral. None when the row has no long form (ḷ)."""
    if not bit_savarna(a, b):
        return None
    out = (a & ~3) | LONG_BIT
    return out if out in NAME_OF else None


def corpus():
    path = os.path.join(HERE, "oracles", "vidyut-sandhi-vowels.tsv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader((l for l in f if not l.startswith("#")), delimiter="\t"):
            a, b, res = r["first_iast"], r["second_iast"], r["result_iast"]
            if a in CELLS and b in CELLS:
                yield a, b, res


def oracle_is_dirgha(a: str, b: str, res: str) -> bool:
    return "|" not in res and res in CELLS and CELLS[res] == ((CELLS[a] & ~3) | LONG_BIT)


ROWS = list(corpus())
def is_diphthong(n): return row(CELLS[n]) >= 5       # e ai o au: not `ak`, so 6.1.101 (akaḥ savarṇe dīrghaḥ) never applies
VARTIKA = {frozenset(("ṛ", "ḷ")), frozenset(("ṝ", "ḷ"))}


def layer_of(a, b):
    k = frozenset((a, b))
    if k in VARTIKA: return 2
    if is_diphthong(a) or is_diphthong(b): return 3
    return 1


class Layer1Sutra(unittest.TestCase):
    def test_predicate_equals_strict_1_1_9_and_vidyut(self):
        n = 0
        for a, b, res in ROWS:
            if layer_of(a, b) != 1:
                continue
            n += 1
            self.assertEqual(bit_savarna(CELLS[a], CELLS[b]), g.savarna(sd.code_of(a), sd.code_of(b)), (a, b))
            self.assertEqual(bit_savarna(CELLS[a], CELLS[b]) and bit_dirgha(CELLS[a], CELLS[b]) is not None,
                             oracle_is_dirgha(a, b, res), (a, b, res))
        self.assertEqual(n, 70)        # measured: 70 ak+ak rows in the pinned corpus, 16 of them merge

    def test_bit_mutation_reproduces_every_vidyut_dirgha_result(self):
        merged = 0
        for a, b, res in ROWS:
            if layer_of(a, b) == 1 and oracle_is_dirgha(a, b, res):
                merged += 1
                self.assertEqual(NAME_OF[bit_dirgha(CELLS[a], CELLS[b])], res, (a, b, res))
        self.assertEqual(merged, 16)


class Layer2Vartika(unittest.TestCase):
    """named, not hidden: ṛ~ḷ."""

    def test_classified_cases(self):
        seen = []
        for a, b, res in ROWS:
            if layer_of(a, b) != 2:
                continue
            seen.append((a, b))
            self.assertFalse(g.savarna(sd.code_of(a), sd.code_of(b)))                  # not by 1.1.9
            self.assertTrue(g.savarna(sd.code_of(a), sd.code_of(b), vartika=True))     # by the vārttika
            self.assertFalse(oracle_is_dirgha(a, b, res))                              # vidyut does not apply it
            self.assertFalse(bit_savarna(CELLS[a], CELLS[b]))                          # Text7 rows differ: agrees with both 1.1.9 and vidyut
        self.assertEqual(set(seen), {("ṛ", "ḷ"), ("ṝ", "ḷ")})


class Layer3WideVowels(unittest.TestCase):
    """named, not hidden: diphthongs. (i) same-letter pairs (e+e): savarṇa by 1.1.9, but 6.1.101 is for `ak` only, so no
    merge: a RULE-SCOPE fact, not a geometry error. (ii) e/ai, o/au: the documented 7-bit limit.
    Corpus coverage: no row has `o` or `ḷ` as the FIRST vowel, so (o,au) is covered by the pair matrix only."""

    def test_classified_cases(self):
        cross = set()
        for a, b, res in ROWS:
            if layer_of(a, b) != 3:
                continue
            self.assertFalse(oracle_is_dirgha(a, b, res), (a, b, res))                 # a diphthong never merges to a long vowel
            if a != b and bit_savarna(CELLS[a], CELLS[b]):
                cross.add((a, b))                                                      # bits say "same row", 1.1.9 says no
        self.assertEqual(cross, {("e", "ai"), ("ai", "e"), ("au", "o")})

    def test_the_limit_is_exactly_one_length_bit(self):
        for lo, hi in (("e", "ai"), ("o", "au")):
            self.assertEqual(CELLS[lo] ^ CELLS[hi], LONG_BIT)


if __name__ == "__main__":
    unittest.main(verbosity=2)
