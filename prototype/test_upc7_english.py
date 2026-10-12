#!/usr/bin/env python3
"""English pilot surface for saṅkṣepa7, without altering 7-bit identities.

English spelling is NOT a one-to-one representation of English speech.
'en' is a restricted Roman phoneme spelling, 'en-ipa' an IPA sound view.
The six /p b k ɡ m ŋ/ candidates and a qualified /j/ system-equivalent
are supported by english-sarvam.yaml;
english-claude-sarvam.yaml disputes labeling English p/k as fully
segment-equivalent because aspiration is contrastive in Sanskrit only.
Therefore this is a research PROFILE, not ratified English.
"""
import unittest

import upc7_geometry as geo
from upc7_layouts import (
    ASSIGNED, RESERVED, UPC7Text, UnassignedSpelling, UnknownSpelling,
    UnrenderableCode, build_cells, build_layouts,
)

CODEC = UPC7Text()
EQUIVALENCES = (
    ("k", "k", geo.varga_code(0, 0)),
    ("ɡ", "g", geo.varga_code(0, 2)),
    ("ŋ", None, geo.varga_code(0, 4)),
    ("p", "p", geo.varga_code(4, 0)),
    ("b", "b", geo.varga_code(4, 2)),
    ("m", "m", geo.varga_code(4, 4)),
    ("j", "y", 0b0100110),  # Sanskrit y; English /j/, not English letter j
)


class EnglishSoundProfileTests(unittest.TestCase):
    def test_new_language_views_exist_without_minting_codes(self):
        self.assertIn("en", build_layouts())
        self.assertIn("en-ipa", build_layouts())
        self.assertEqual(len(CODEC.layout("en").code_to_spelling), 8)
        self.assertEqual(len(CODEC.layout("en-ipa").code_to_spelling), 9)
        cells = {c.code: c for c in build_cells()}
        self.assertEqual(len(cells), 128)
        self.assertEqual(sum(c.status == RESERVED for c in cells.values()), 21)
        for _ipa, _roman, code in EQUIVALENCES:
            self.assertEqual(cells[code].status, ASSIGNED)
            self.assertEqual(len(geo.code_bits(code)), 7)

    def test_individual_admitted_sounds_are_injective_and_roundtrip(self):
        for ipa, roman, code in EQUIVALENCES:
            with self.subTest(ipa=ipa):
                self.assertEqual(CODEC.encode(ipa, "en-ipa"), (code,))
                self.assertEqual(CODEC.render([code], "en-ipa"), ipa)
                if roman is None:
                    with self.assertRaises(UnrenderableCode):
                        CODEC.render([code], "en")
                else:
                    self.assertEqual(CODEC.encode(roman, "en"), (code,))
                    self.assertEqual(CODEC.render([code], "en"), roman)

    def test_sanskrit_keeps_its_own_script_without_code_reallocation(self):
        for ipa, roman, code in EQUIVALENCES:
            with self.subTest(ipa=ipa):
                expected = CODEC.render([code], "sa-iast")
                self.assertEqual(
                    CODEC.encode(expected, "sa-iast"), (code,)
                )
                self.assertEqual(
                    CODEC.switch_layout(ipa, "en-ipa", "sa-iast"), expected
                )
        self.assertEqual(CODEC.switch_layout("b", "en", "uk"), "б")
        self.assertEqual(CODEC.switch_layout("ŋ", "en-ipa", "sa-iast"), "ṅ")

    def test_fail_closed_on_english_false_friends_and_unplaced_sounds(self):
        for spelling in ("th", "sh", "ch", "f", "v", "w", "t", "d", "n",
                         "a", "e", "i", "o", "u", "θ", "ð", "ə", "æ",
                         "ʊ", "ɪ", "ʒ", "ʃ"):
            with self.subTest(spelling=spelling):
                with self.assertRaises((UnassignedSpelling, UnknownSpelling)):
                    CODEC.encode(spelling, "en")
        # In Sanskrit, 'th' is a stop with contrastive aspiration.
        self.assertEqual(CODEC.encode("th", "sa-iast"), (geo.varga_code(3, 1),))
        with self.assertRaises((UnassignedSpelling, UnknownSpelling)):
            CODEC.encode("th", "en")

    def test_space_and_period_are_text_data_not_phonemes(self):
        space = geo.sign_code("space")
        period = geo.sign_code("dot")
        self.assertNotEqual(space, period)
        for language in ("en", "en-ipa"):
            with self.subTest(language=language):
                self.assertEqual(CODEC.encode(" ", language), (space,))
                self.assertEqual(CODEC.encode(".", language), (period,))
                self.assertEqual(CODEC.render_checked((space, period), language), " .")
                sample = "b. m"
                expected = (
                    geo.varga_code(4, 2), period, space, geo.varga_code(4, 4)
                )
                self.assertEqual(CODEC.encode(sample, language), expected)
                self.assertEqual(CODEC.render_checked(expected, language), sample)
                self.assertEqual(CODEC.encode("b..m", language), (
                    geo.varga_code(4, 2), period, period, geo.varga_code(4, 4)
                ))
        self.assertEqual(CODEC.switch_layout("b. m", "en", "uk"), "б. м")

    def test_reserved_and_other_sign_cells_are_still_unrenderable(self):
        text_signs = {geo.sign_code("space"), geo.sign_code("dot")}
        for cell in build_cells():
            if (cell.status == RESERVED or cell.klass == "sign/operator") and cell.code not in text_signs:
                for name in ("en", "en-ipa"):
                    with self.subTest(name=name, code=cell.code):
                        with self.assertRaises(UnrenderableCode):
                            CODEC.render([cell.code], name)

    def test_no_silent_uppercase_alias_or_english_orthography_claim(self):
        for text in ("K", "P", "king", "think", "the", "queue", "ng"):
            with self.subTest(text=text):
                with self.assertRaises((UnassignedSpelling, UnknownSpelling)):
                    CODEC.encode(text, "en")
        self.assertEqual(CODEC.encode("gbmpk", "en"), tuple(
            CODEC.layout("en").spelling_to_code[c] for c in "gbmpk"
        ))
        self.assertEqual(
            CODEC.render(CODEC.encode("gbmpk", "en"), "en"), "gbmpk"
        )


if __name__ == "__main__":
    unittest.main()
