#!/usr/bin/env python3
"""First Round-Trip Sandhi Suite: Guṇa and Vṛddhi Mutations over 7-bit Text7 Codes.

Demonstrates:
  1. Pure bitwise sandhi mutation: Pāṇini 6.1.87 (ād guṇaḥ) and 6.1.88 (vṛddhireci).
     Operates directly on 7-bit cells via class, place, and row bitfields.
  2. Domain demarcation: Zero grammatical numbers in Text7 codes.
  3. Multi-script round-trip:
     word1 + word2 -> Text7 cells -> bit mutation at junction -> decoded surface word
     tested across scientific IAST, native Devanagari, and Ukrainian Cyrillic.

Zero external dependencies. Pure Python standard library.
"""

from __future__ import annotations

import os
import sys
import unittest
from typing import List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import upc7_lang as L

TEXT = L.LangText()

# Bit constants for Text7 vowel geometry
CLASS_VOWEL = 0b10
ROW_A = 0       # Kaṇṭhya
ROW_I = 1       # Tālavya
ROW_U = 2       # Oṣṭhya
ROW_R = 3       # Mūrdhanya
ROW_L = 4       # Dantya
ROW_E = 5       # Kaṇṭha-Tālavya (guṇa of i)
ROW_O = 6       # Kaṇṭha-Oṣṭhya (guṇa of u)

CELL_A = (CLASS_VOWEL << 5) | (ROW_A << 2)      # 01000000 = 64
CELL_E = (CLASS_VOWEL << 5) | (ROW_E << 2)      # 01010100 = 84
CELL_O = (CLASS_VOWEL << 5) | (ROW_O << 2)      # 01011000 = 88
CELL_AI = CELL_E | 1                            # 01010101 = 85 (long/wide form of row E)
CELL_AU = CELL_O | 1                            # 01011001 = 89 (long/wide form of row O)

# Non-varga sonorants for raparaḥ / laparaḥ (P.1.1.51)
CELL_R = (0b01 << 5) | (2 << 2) | 2             # 0101010 = 42 (Mūrdhanya sonorant)
CELL_L = (0b01 << 5) | (3 << 2) | 2             # 0101110 = 46 (Dantya sonorant)


def is_vowel_cell(c: int) -> bool:
    return (c >> 5) == CLASS_VOWEL


def vowel_row(c: int) -> int:
    return (c & 31) >> 2


def is_a_vowel(c: int) -> bool:
    """True for short a or long ā (row 0)."""
    return is_vowel_cell(c) and vowel_row(c) == ROW_A


def mutate_guna_vriddhi_junction(c1: int, c2: int) -> Optional[Tuple[int, ...]]:
    """Mutates junction vowels (c1 + c2) strictly by bit operations.
    Returns replacement cell tuple, or None if rule does not trigger.
    """
    if not (is_vowel_cell(c1) and is_vowel_cell(c2)):
        return None

    # Precondition: c1 must be a-vowel (a or ā)
    if not is_a_vowel(c1):
        return None

    row2 = vowel_row(c2)

    # 1. Pāṇini 6.1.88: vṛddhireci (a + e/ai/o/au -> vṛddhi)
    if row2 == ROW_E:
        return (CELL_AI,)
    if row2 == ROW_O:
        return (CELL_AU,)

    # 2. Pāṇini 6.1.87: ād guṇaḥ (a + i/u/ṛ/ḷ -> guṇa)
    if row2 == ROW_I:
        return (CELL_E,)
    if row2 == ROW_U:
        return (CELL_O,)
    if row2 == ROW_R:
        # P.1.1.51: uraṇ raparaḥ -> a followed by r
        return (CELL_A, CELL_R)
    if row2 == ROW_L:
        # a followed by l
        return (CELL_A, CELL_L)

    return None


def apply_sandhi_word_junction(word1: str, word2: str, layout: str = "sa-iast") -> str:
    """Encodes two words to 7-bit cells, applies bitwise junction mutation, and renders."""
    cells1 = TEXT.encode(word1, layout)
    cells2 = TEXT.encode(word2, layout)

    assert len(cells1) > 0 and len(cells2) > 0, "Words must yield non-empty cell streams"

    # Find junction
    last1 = cells1[-1]
    first2 = cells2[0]

    mutation = mutate_guna_vriddhi_junction(last1, first2)
    if mutation is None:
        merged_cells = cells1 + cells2
    else:
        merged_cells = cells1[:-1] + mutation + cells2[1:]

    return TEXT.render(merged_cells, layout)


class TestGunaVriddhiSandhiRoundtrip(unittest.TestCase):
    """Test suite verifying bit-level sandhi round-tripping across authentic examples."""

    def test_guna_a_plus_i(self):
        # deva + indra -> devendra
        res_iast = apply_sandhi_word_junction("deva", "indra", "sa-iast")
        self.assertEqual(res_iast, "devendra")

        res_deva = apply_sandhi_word_junction("देव", "इन्द्र", "sa-deva")
        self.assertEqual(res_deva, "देवेन्द्र")

        res_cyr = apply_sandhi_word_junction("дева", "індра", "sa-cyr")
        self.assertEqual(res_cyr, "девендра")

    def test_guna_aa_plus_long_i(self):
        # mahā + īśa -> maheśa
        res_iast = apply_sandhi_word_junction("mahā", "īśa", "sa-iast")
        self.assertEqual(res_iast, "maheśa")

        res_deva = apply_sandhi_word_junction("महा", "ईश", "sa-deva")
        self.assertEqual(res_deva, "महेश")

    def test_guna_a_plus_u(self):
        # sūrya + udaya -> sūryodaya
        res_iast = apply_sandhi_word_junction("sūrya", "udaya", "sa-iast")
        self.assertEqual(res_iast, "sūryodaya")

        res_deva = apply_sandhi_word_junction("सूर्य", "उदय", "sa-deva")
        self.assertEqual(res_deva, "सूर्योदय")

        res_cyr = apply_sandhi_word_junction("сӯрйа", "удайа", "sa-cyr")
        self.assertEqual(res_cyr, "сӯрйодайа")

    def test_guna_aa_plus_u(self):
        # gaṅgā + udakam -> gaṅgodakam
        res_iast = apply_sandhi_word_junction("gaṅgā", "udakam", "sa-iast")
        self.assertEqual(res_iast, "gaṅgodakam")

        res_deva = apply_sandhi_word_junction("गङ्गा", "उदकम्", "sa-deva")
        self.assertEqual(res_deva, "गङ्गोदकम्")

    def test_guna_aa_plus_ri_raparah(self):
        # mahā + ṛṣi -> maharṣi (with uraṇ raparaḥ)
        res_iast = apply_sandhi_word_junction("mahā", "ṛṣi", "sa-iast")
        self.assertEqual(res_iast, "maharṣi")

        res_deva = apply_sandhi_word_junction("महा", "ऋषि", "sa-deva")
        self.assertEqual(res_deva, "महर्षि")

    def test_guna_a_plus_lri(self):
        # tava + ḷkāra -> tavalkāra
        res_iast = apply_sandhi_word_junction("tava", "ḷkāra", "sa-iast")
        self.assertEqual(res_iast, "tavalkāra")

        res_deva = apply_sandhi_word_junction("तव", "ऌकार", "sa-deva")
        self.assertEqual(res_deva, "तवल्कार")

    def test_vriddhi_a_plus_e(self):
        # adya + eva -> adyaiva
        res_iast = apply_sandhi_word_junction("adya", "eva", "sa-iast")
        self.assertEqual(res_iast, "adyaiva")

        res_deva = apply_sandhi_word_junction("अद्य", "एव", "sa-deva")
        self.assertEqual(res_deva, "अद्यैव")

    def test_vriddhi_a_plus_ai(self):
        # deva + aiśvarya -> devaiśvarya
        res_iast = apply_sandhi_word_junction("deva", "aiśvarya", "sa-iast")
        self.assertEqual(res_iast, "devaiśvarya")

        res_deva = apply_sandhi_word_junction("देव", "ऐश्वर्य", "sa-deva")
        self.assertEqual(res_deva, "देवैश्वर्य")

    def test_vriddhi_a_plus_o(self):
        # jala + ogha -> jalaugha
        res_iast = apply_sandhi_word_junction("jala", "ogha", "sa-iast")
        self.assertEqual(res_iast, "jalaugha")

        res_deva = apply_sandhi_word_junction("जल", "ओघ", "sa-deva")
        self.assertEqual(res_deva, "जलौघ")


if __name__ == "__main__":
    unittest.main()
