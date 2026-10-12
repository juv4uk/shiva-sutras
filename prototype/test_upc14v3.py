#!/usr/bin/env python3
"""UPC-14 v3 English: owner-independent source inventory and bit-law witnesses.

Standard-library-only, no SENS import and no mutation of UPC-14 v2.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import unittest

import upc14v2 as v2
import upc14v3 as v3


HERE = Path(__file__).resolve().parent
EXTENSIONS = HERE.parent / "extensions"


def donor_ipa(path: Path) -> tuple[str, ...]:
    """Pull ONLY IPA fields beneath the 44 explicit PH-ENG donor blocks."""
    source = path.read_text(encoding="utf-8")
    blocks = re.split(r"(?=^  - id: PH-ENG-)", source, flags=re.MULTILINE)
    values = []
    for block in blocks:
        if not block.startswith("  - id: PH-ENG-"):
            continue
        ipa = re.search(r"^\s*ipa:\s*\"?([^\"\n]+)\"?\s*$", block, flags=re.MULTILINE)
        if ipa is None:
            raise AssertionError(f"{path} has a phoneme with no IPA")
        values.append(ipa.group(1).strip().strip('"'))
    return tuple(values)


class EnglishInventoryTests(unittest.TestCase):
    def test_all_44_phonemes_are_present_exactly_once(self) -> None:
        self.assertEqual(len(v3.ENGLISH), 44)
        self.assertEqual(len({row.ipa for row in v3.ENGLISH}), 44)
        self.assertEqual(len({row.code for row in v3.ENGLISH}), 44)
        self.assertEqual(Counter(row.family for row in v3.ENGLISH),
                         {"consonant": 24, "vowel": 20})
        self.assertEqual(sum(row.features is None for row in v3.ENGLISH), 7)
        self.assertEqual(sum(row.features is not None for row in v3.ENGLISH), 37)

    def test_both_independent_english_reference_inventories(self) -> None:
        sarvam = set(donor_ipa(EXTENSIONS / "english-sarvam.yaml"))
        claude = set(donor_ipa(EXTENSIONS / "english-claude-sarvam.yaml"))
        # The donor sources use alternate representations of affricates:
        # IPA tie bars vs retracted postalveolar stop + fricative.
        normalized = {"t͡ʃ" if x == "t̠ʃ" else
                      "d͡ʒ" if x == "d̠ʒ" else x for x in claude}
        self.assertEqual((len(sarvam), len(claude)), (44, 44))
        self.assertEqual(sarvam, {row.ipa for row in v3.ENGLISH})
        self.assertEqual(normalized, sarvam)

    def test_roundtrip_exact_on_all_44_14bit_sound_words(self) -> None:
        for row in v3.ENGLISH:
            with self.subTest(row=row.ipa):
                self.assertEqual(v3.encode_english_phoneme(row.ipa), row.code)
                self.assertEqual(v3.decode_english_phoneme(row.code), row.ipa)
                self.assertEqual(len(v3.bitstring(row.code)), 14)
                if row.features is not None:
                    self.assertEqual(v3.unpack_extension(row.code), row.features)
                    self.assertEqual(row.code >> 12, 0b11)
                else:
                    self.assertEqual(row.code, v2.SOUNDS[row.v2_label])
                    self.assertEqual(row.code >> 13, 0)

    def test_v2_42_sound_codes_and_all_marker_nodes_are_immutable(self) -> None:
        self.assertEqual(len(v2.SOUNDS), 42)
        v3_codes = {row.code for row in v3.ENGLISH if row.features is not None}
        self.assertTrue(v3_codes.isdisjoint(set(v2.SOUNDS.values())))
        for marker in v2.it_ranks():
            word = v2.meta_code(marker)
            self.assertEqual(word >> 12, 0b10)
            self.assertNotIn(word, v3_codes)
            with self.assertRaises(v3.UPC14V3Error):
                v3.decode_english_phoneme(word)

    def test_no_english_false_friend_silently_reuses_sanskrit(self) -> None:
        for ipa in ("t", "d", "f", "v", "θ", "ð", "s", "z",
                    "ʃ", "ʒ", "h", "n", "w", "ɹ", "l",
                    "ɪ", "e", "æ", "ɒ", "ʌ", "ʊ", "ə"):
            with self.subTest(ipa=ipa):
                code = v3.encode_english_phoneme(ipa)
                self.assertNotIn(code, v2.SOUNDS.values())
                self.assertEqual(code >> 12, 0b11)
        # Sanskrit v is a semivowel; English v a labiodental fricative.
        self.assertNotEqual(v3.encode_english_phoneme("v"), v2.SOUNDS["v"])
        # English alveolar t/d must NOT coincide with Sanskrit dental t/d.
        self.assertNotEqual(v3.encode_english_phoneme("t"), v2.SOUNDS["t"])
        self.assertNotEqual(v3.encode_english_phoneme("d"), v2.SOUNDS["d"])

    def test_feature_bit_laws_form_minimal_pair_edges(self) -> None:
        voice_mask = 1 << 3
        for left, right in (("t", "d"), ("θ", "ð"), ("s", "z"),
                            ("f", "v"), ("ʃ", "ʒ"), ("t͡ʃ", "d͡ʒ")):
            self.assertEqual(v3.encode_english_phoneme(left) ^
                             v3.encode_english_phoneme(right), voice_mask)
        self.assertNotEqual(v3.encode_english_phoneme("ɪ"),
                            v3.encode_english_phoneme("iː"))
        self.assertNotEqual(v3.encode_english_phoneme("eɪ"),
                            v3.encode_english_phoneme("eə"))

    def test_exhaustive_extension_bit_inverse_and_admission_gate(self) -> None:
        admitted_extensions = {row.code for row in v3.ENGLISH
                               if row.features is not None}
        self.assertEqual(len(admitted_extensions), 37)
        for code in range(0x3000, 0x4000):
            try:
                features = v3.unpack_extension(code)
            except v3.UPC14V3Error:
                self.assertNotIn(code, admitted_extensions)
                continue
            if isinstance(features, v3.ConsonantFeatures):
                self.assertEqual(v3.pack_consonant(features), code)
            else:
                self.assertEqual(v3.pack_vowel(features), code)
            if code not in admitted_extensions:
                with self.assertRaises(v3.UPC14V3Error):
                    v3.decode_english_phoneme(code)

    def test_legacy_seven_bit_path_only_for_verified_sound_ancestry(self) -> None:
        expected = {
            "k": 0b0000000, "ɡ": 0b0000010, "ŋ": 0b0000100,
            "p": 0b0010100, "b": 0b0010110, "m": 0b0011000,
            "j": 0b0100110,
        }
        for ipa, seven in expected.items():
            self.assertEqual(v3.project_to_legacy_upc7(ipa), seven)
        for row in v3.ENGLISH:
            if row.ipa not in expected:
                self.assertIsNone(v3.project_to_legacy_upc7(row.ipa))

    def test_unsupported_tokens_fail_closed_no_orthographic_fallback(self) -> None:
        for spelling in ("th", "TH", "phone", "g", "y", "a", "tʃ", "dʒ",
                         "t", "d", "æ̀", ""):
            # "t"/"d" *are* phonemes, not orthographic spellings to reject.
            if spelling in ("t", "d"):
                continue
            with self.subTest(spelling=spelling):
                with self.assertRaises(v3.UPC14V3Error):
                    v3.encode_english_phoneme(spelling)
        for number in (-1, 0x4000, 0x2000, 0x3010, 0x3810, "0", None):
            with self.subTest(number=number):
                if number in {0x3010, 0x3810}:
                    # These happen to be valid feature vertices, but never
                    # admitted into the English inventory.
                    self.assertNotIn(number, {r.code for r in v3.ENGLISH})
                with self.assertRaises(v3.UPC14V3Error):
                    v3.decode_english_phoneme(number)

    def test_v2_can_still_be_queried_with_its_original_graph_laws(self) -> None:
        self.assertEqual(v2.e_asp(v2.SOUNDS["k"]), v2.SOUNDS["kh"])
        self.assertEqual(v2.e_voice(v2.SOUNDS["k"]), v2.SOUNDS["g"])
        self.assertEqual(v2.e_nasal(v2.SOUNDS["g"]), v2.SOUNDS["ṅ"])


if __name__ == "__main__":
    unittest.main()
