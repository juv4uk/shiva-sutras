#!/usr/bin/env python3
"""Exhaustive (depth 1 & 2) exact-7-bit reversibility check for all languages.

The distinction matters:
- cell -> script -> cell may be bijective for a single spelling;
- a concatenation may merge boundaries: k+h == kh, д+ж == дж;
- changing case / Ukrainian iotated orthography may canonicalize spelling.
A returned cross-language string MUST re-encode to identical exact cells.
"""
from __future__ import annotations

import unittest

import upc7_geometry as geo
from upc7_layouts import UPC7Text, UnrenderableCode, UnknownSpelling, UnassignedSpelling, build_cells
import upc7_lang

GEOMETRY = UPC7Text()
ORTHOGRAPHY = upc7_lang.LangText()


class ReversibilityAudit(unittest.TestCase):
    def test_every_direct_cell_of_every_geometry_language_is_reversible(self):
        for language, layout in GEOMETRY.layouts.items():
            with self.subTest(language=language):
                for cell, spelling in layout.code_to_spelling.items():
                    self.assertEqual(
                        GEOMETRY.render_checked((cell,), language), spelling
                    )
                    self.assertEqual(GEOMETRY.encode(spelling, language), (cell,))
        for c in build_cells():
            bits = geo.code_bits(c.code)
            self.assertEqual(GEOMETRY.render_checked((c.code,), "bits"), bits)
            self.assertEqual(GEOMETRY.encode(bits, "bits"), (c.code,))

    def test_every_direct_two_cell_sequence_is_either_exact_or_refused(self):
        for language, layout in GEOMETRY.layouts.items():
            codes = tuple(layout.code_to_spelling)
            accepted = refused = 0
            for a in codes:
                for b in codes:
                    try:
                        text = GEOMETRY.render_checked((a, b), language)
                    except UnrenderableCode:
                        refused += 1
                    else:
                        accepted += 1
                        self.assertEqual(GEOMETRY.encode(text, language), (a, b))
            self.assertEqual(accepted + refused, len(codes) ** 2)
            self.assertGreater(accepted, 0)
            print(
                f"UPC7-BIJECTION {language}: {len(codes)} direct glyphs, "
                f"{accepted} exact pairs, {refused} refused ambiguities",
                flush=True,
            )

    def test_every_two_cell_token_stream_roundtrips_in_every_language(self):
        for language, layout in GEOMETRY.layouts.items():
            codes = tuple(layout.code_to_spelling)
            for a in codes:
                for b in codes:
                    with self.subTest(language=language, a=a, b=b):
                        pair = (a, b)
                        spellings = GEOMETRY.render_tokens(pair, language)
                        self.assertEqual(
                            GEOMETRY.encode_tokens(spellings, language), pair
                        )

        for code in range(128):
            bits = (geo.code_bits(code),)
            self.assertEqual(GEOMETRY.render_tokens((code,), "bits"), bits)
            self.assertEqual(GEOMETRY.encode_tokens(bits, "bits"), (code,))

    def test_token_stream_exposes_ambiguous_boundaries_without_renumbering(self):
        for language, phrase in (
            ("sa-iast", ("k", "h")),
            ("sa-iast", ("a", "i")),
            ("sa-slp1", (".", ".")),
            ("uk", ("д", "ж")),
            ("uk", ("д", "з")),
        ):
            with self.subTest(language=language, phrase=phrase):
                original = GEOMETRY.encode_tokens(phrase, language)
                self.assertEqual(GEOMETRY.render_tokens(original, language), phrase)
                self.assertEqual(GEOMETRY.encode_tokens(phrase, language), original)
                self.assertNotEqual(
                    GEOMETRY.encode("".join(phrase), language), original
                )

    def test_space_and_period_are_text_cells_not_reader_controls(self):
        space = geo.sign_code("space")
        dot = geo.sign_code("dot")
        for language in ("uk", "sa-iast", "sa-deva", "en", "en-ipa"):
            with self.subTest(language=language):
                self.assertEqual(GEOMETRY.encode(" .", language), (space, dot))
                self.assertEqual(
                    GEOMETRY.render_checked((space, dot), language), " ."
                )
                self.assertEqual(
                    GEOMETRY.encode_tokens((" ", "."), language), (space, dot)
                )
        # SLP1 historically spells Sanskrit daṇḍa with "."; it is a
        # DIFFERENT seven-bit cell from the ASCII text period. Never equate
        # these two identities just because their human glyph matches.
        danda = geo.sign_code("danda")
        self.assertNotEqual(danda, dot)
        self.assertEqual(GEOMETRY.encode(".", "sa-slp1"), (danda,))
        self.assertEqual(GEOMETRY.encode(" ", "sa-slp1"), (space,))
        with self.assertRaises(UnrenderableCode):
            GEOMETRY.render_checked((space, dot), "sa-slp1")
        with self.assertRaises(UnrenderableCode):
            GEOMETRY.switch_layout(".", "en", "sa-slp1")

    def test_known_sanskrit_and_ukrainian_boundary_collisions_are_refused(self):
        for language, source in (
            ("sa-iast", ("k", "h")),
            ("sa-iast", ("a", "i")),
            ("sa-iast", ("t", "h")),
            ("sa-slp1", (".", ".")),
            ("uk", ("д", "ж")),
            ("uk", ("д", "з")),
        ):
            with self.subTest(language=language, source=source):
                individual = tuple(
                    GEOMETRY.encode(part, language)[0] for part in source
                )
                text = GEOMETRY.render(individual, language)
                self.assertEqual(text, "".join(source))
                self.assertNotEqual(GEOMETRY.encode(text, language), individual)
                with self.assertRaises(UnrenderableCode):
                    GEOMETRY.render_checked(individual, language)

    def test_all_language_switches_preserve_exact_cells_or_refuse(self):
        # Including both English views and all three Sanskrit views.
        for source_name, source in GEOMETRY.layouts.items():
            for target_name in GEOMETRY.layouts:
                with self.subTest(source=source_name, target=target_name):
                    witnessed = 0
                    for code, spelling in source.code_to_spelling.items():
                        try:
                            switched = GEOMETRY.switch_layout(
                                spelling, source_name, target_name
                            )
                        except UnrenderableCode:
                            continue
                        self.assertEqual(
                            GEOMETRY.encode(switched, target_name), (code,)
                        )
                        witnessed += 1
                    if source_name == target_name:
                        self.assertEqual(witnessed, len(source.code_to_spelling))

    def test_ukrainian_orthography_and_case_are_not_bijective_source_spelling(self):
        # Sound7 preserved phonemes, NOT an exact copy of every input spelling.
        original = "я"
        encoded = GEOMETRY.encode(original, "uk")
        displayed = GEOMETRY.render_checked(encoded, "uk")
        self.assertEqual(displayed, "йа")
        self.assertEqual(GEOMETRY.encode(displayed, "uk"), encoded)
        self.assertNotEqual(displayed, original)
        self.assertEqual(GEOMETRY.encode("Кіт", "uk"),
                         GEOMETRY.encode("кіт", "uk"))

    def test_richer_language_codec_handles_all_existing_language_profiles(self):
        for language in upc7_lang.LAYOUTS:
            admitted = 0
            for cell in range(128):
                try:
                    text = ORTHOGRAPHY.render((cell,), language)
                except upc7_lang.LangError:
                    continue
                self.assertEqual(ORTHOGRAPHY.encode(text, language), (cell,))
                admitted += 1
            self.assertGreater(admitted, 0)
            print(f"UPC7-LANGUAGE {language}: {admitted} exact singleton cells",
                  flush=True)

    def test_extended_ukrainian_capital_and_iotated_orthography(self):
        for example in ("Кіт", "Україна", "щасливий", "джміль", "сім'я"):
            with self.subTest(example=example):
                codes = ORTHOGRAPHY.encode(example, "uk")
                self.assertEqual(ORTHOGRAPHY.render(codes, "uk"), example)

    def test_english_renders_only_admitted_pilot_phoneme_cells(self):
        for sound in ("b", "ɡ", "k", "m", "p", "ŋ", "j"):
            codes = GEOMETRY.encode(sound, "en-ipa")
            self.assertEqual(GEOMETRY.render_checked(codes, "en-ipa"), sound)
        for sound in ("θ", "ð", "æ", "ə", "ɪ", "ʃ"):
            with self.assertRaises((UnknownSpelling, UnassignedSpelling)):
                GEOMETRY.encode(sound, "en-ipa")


if __name__ == "__main__":
    unittest.main()
