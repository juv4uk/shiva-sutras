#!/usr/bin/env python3
"""Witnesses for the UPC-7 layouts built on geometry v2 (shiva-sutras#29)."""

import re
import unittest

import upc7_geometry as geo
from upc7_layouts import (
    ASSIGNED,
    RESERVED,
    Layout,
    UPC7LayoutError,
    UPC7Text,
    UnassignedSpelling,
    UnknownLayout,
    UnknownSpelling,
    UnrenderableCode,
    build_cells,
)
from upc7_table import TABLE_PATH, render_table
from upc8 import CODE_OF_SOUND, UKRAINIAN_SHARED, UPC8

CODEC = UPC7Text()
SANSKRIT = CODEC.layout("sa-slp1")
UKRAINIAN = CODEC.layout("uk")

# Ukrainian spellings the geometry gives a cell today (see UPC7.md, "Gaps").
UKRAINIAN_PLACED = set("кґтднпбм" + "іу" + "хшжйзсрлфвг") | {"а", "е", "о", "и", "ц", "ч", "дз", "дж", "ь"}


def unescape(field: str) -> str:
    return re.sub(
        r"\\(\\|x[0-9a-fA-F]{2})",
        lambda m: "\\" if m.group(1) == "\\" else chr(int(m.group(1)[1:], 16)),
        field,
    )


class CellTableTests(unittest.TestCase):
    def test_there_is_one_cell_per_code_in_order(self):
        cells = build_cells()
        self.assertEqual([cell.code for cell in cells], list(range(128)))

    def test_assigned_and_reserved_counts_are_pinned(self):
        counts = {}
        for cell in build_cells():
            key = (cell.klass, cell.status)
            counts[key] = counts.get(key, 0) + 1
        self.assertEqual(
            counts,
            {
                ("varga", ASSIGNED): 25,
                ("varga", RESERVED): 7,
                ("non-varga", ASSIGNED): 18,
                ("non-varga", RESERVED): 14,
                ("vowel", ASSIGNED): 32,
                ("sign/operator", ASSIGNED): 32,
            },
        )

    def test_identity_names_are_unique(self):
        names = [cell.name for cell in build_cells()]
        self.assertEqual(len(names), len(set(names)))

    def test_reserved_cells_are_exactly_the_unplaced_ones(self):
        for cell in build_cells():
            reserved = cell.status == RESERVED
            self.assertEqual(reserved, cell.name.startswith("reserved."), cell)


class LayoutShapeTests(unittest.TestCase):
    def test_unknown_layout_is_rejected(self):
        with self.assertRaises(UnknownLayout):
            CODEC.layout("klingon")

    def test_a_layout_cannot_name_two_codes_with_one_spelling(self):
        with self.assertRaises(UPC7LayoutError):
            Layout("broken", {0: "x", 1: "x"})

    def test_a_spelling_cannot_be_both_assigned_and_unassigned(self):
        with self.assertRaises(UPC7LayoutError):
            Layout("broken", {0: "x"}, frozenset({"x"}))

    def test_spelling_counts_are_pinned(self):
        # 25 varga + 8 non-varga + 14 oral vowels + 5 Sanskrit signs + 25 ASCII signs
        self.assertEqual(len(SANSKRIT.code_to_spelling), 25 + 8 + 14 + 5 + 25)
        # 8 varga + 11 non-varga + 2 aliased vowels + 27 ASCII signs
        # + 4 extension vowels + 4 affricates + 1 softness (shiva-sutras#31)
        self.assertEqual(len(UKRAINIAN.code_to_spelling), 8 + 11 + 2 + 27 + 4 + 4 + 1)

    def test_every_layout_spelling_names_an_assigned_cell(self):
        status = {cell.code: cell.status for cell in build_cells()}
        for layout in (SANSKRIT, UKRAINIAN):
            for code in layout.code_to_spelling:
                self.assertEqual(status[code], ASSIGNED, (layout.name, code))


class SanskritCoverageTests(unittest.TestCase):
    def test_all_42_canonical_sounds_have_a_spelling_and_a_cell(self):
        spelled = SANSKRIT.spelling_to_code
        for slp1 in CODE_OF_SOUND:
            self.assertIn(slp1, spelled, slp1)

    def test_long_vowels_anusvara_and_visarga(self):
        for letter in "AIUFXMH":
            self.assertIn(letter, SANSKRIT.spelling_to_code, letter)

    def test_sanskrit_words_round_trip_through_codes_and_bits(self):
        for word in ("kim", "rAma", "kfzRa", "saMskftam", "namaH", "Darma"):
            codes = CODEC.encode(word, "sa-slp1")
            self.assertEqual(CODEC.render(codes, "sa-slp1"), word)
            bits = CODEC.render(codes, "bits")
            self.assertEqual(CODEC.encode(bits, "bits"), codes)
            self.assertEqual(CODEC.switch_layout(bits, "bits", "sa-slp1"), word)

    def test_every_varga_cell_is_reachable_by_its_slp1_letter(self):
        for place, letters in enumerate("kKgGN cCjJY wWqQR tTdDn pPbBm".split()):
            for member, letter in enumerate(letters):
                self.assertEqual(
                    CODEC.encode(letter, "sa-slp1"), (geo.varga_code(place, member),)
                )

    def test_ai_and_au_are_the_long_forms_of_e_and_o(self):
        self.assertEqual(CODEC.encode("E", "sa-slp1"), (geo.vowel_code(5, length=True),))
        self.assertEqual(CODEC.encode("O", "sa-slp1"), (geo.vowel_code(6, length=True),))


class UkrainianTests(unittest.TestCase):
    def test_exactly_the_placed_letters_are_spelled(self):
        letters = {s for s in UKRAINIAN.spelling_to_code if all("\u0400" <= c <= "\u04ff" for c in s)}
        self.assertEqual(letters, UKRAINIAN_PLACED)

    def test_donor_identity_aliases_share_the_sanskrit_code(self):
        # The donor marks these 13 Ukrainian letters as segment-/system-equivalents
        # of a Sanskrit sound. On geometry v2 they must land on the same cell.
        donor = UPC8().table
        for _, letter, _, shared_code, _, _ in UKRAINIAN_SHARED:
            slp1 = donor[shared_code]["slp1"]
            self.assertEqual(
                CODEC.encode(letter, "uk"), CODEC.encode(slp1, "sa-slp1"), (letter, slp1)
            )

    def test_placed_words_switch_layout_without_changing_codes(self):
        for word, sanskrit in (("кіт", "kit"), ("кум", "kum"), ("ніс", "nis"), ("тут", "tut")):
            codes = CODEC.encode(word, "uk")
            self.assertEqual(CODEC.switch_layout(word, "uk", "sa-slp1"), sanskrit)
            self.assertEqual(CODEC.encode(sanskrit, "sa-slp1"), codes)

    def test_extension_sounds_have_their_own_cells(self):
        # shiva-sutras#31: а е о и, ц ч дз дж and ь are cells of their own.
        singles = ("а", "е", "о", "и", "ц", "ч", "дз", "дж", "ь")
        codes = [CODEC.encode(s, "uk") for s in singles]
        for s, c in zip(singles, codes):
            self.assertEqual(len(c), 1, s)
        self.assertEqual(len({c[0] for c in codes}), len(singles))  # injective
        for s, c in zip(singles, codes):
            self.assertEqual(CODEC.render(c, "uk"), s)

    def test_words_that_used_to_fail_now_encode_and_round_trip(self):
        for word in ("привіт", "мама", "цар", "час", "дзвін", "джміль", "тінь", "сіль"):
            codes = CODEC.encode(word, "uk")
            self.assertEqual(CODEC.render(codes, "uk"), word, word)

    def test_iotated_vowels_and_shch_are_sequences_not_cells(self):
        iota = CODEC.encode("й", "uk")
        self.assertEqual(CODEC.encode("я", "uk"), iota + CODEC.encode("а", "uk"))
        self.assertEqual(CODEC.encode("ю", "uk"), iota + CODEC.encode("у", "uk"))
        self.assertEqual(CODEC.encode("є", "uk"), iota + CODEC.encode("е", "uk"))
        self.assertEqual(CODEC.encode("ї", "uk"), iota + CODEC.encode("і", "uk"))
        self.assertEqual(CODEC.encode("щ", "uk"), CODEC.encode("шч", "uk"))
        # They never render back as one letter: `я` and `йа` are one code stream.
        self.assertEqual(CODEC.render(CODEC.encode("я", "uk"), "uk"), "йа")

    def test_palatalised_consonant_is_consonant_plus_softness(self):
        self.assertEqual(
            CODEC.encode("ть", "uk"), CODEC.encode("т", "uk") + CODEC.encode("ь", "uk")
        )
        self.assertEqual(len(CODEC.encode("ль", "uk")), 2)

    def test_affricate_is_one_cell_not_a_pair_of_letters(self):
        self.assertEqual(len(CODEC.encode("дж", "uk")), 1)
        self.assertNotEqual(CODEC.encode("дж", "uk"), CODEC.encode("д", "uk") + CODEC.encode("ж", "uk"))
        self.assertEqual(len(CODEC.encode("дз", "uk")), 1)

    def test_extension_cells_are_invisible_to_sanskrit_predicates(self):
        # Row 7 has its own indexing; rows 0..6 (ac, aṇ, ik ...) are untouched.
        for index in range(4):
            code = geo.uk_ext_vowel_code(index)
            self.assertEqual(geo.payload_of(code) >> 2, 7)
            with self.assertRaises(geo.UPC7GeometryError):
                geo.decode_vowel(code)

    def test_sanskrit_and_earlier_ukrainian_codes_are_unchanged(self):
        # Adding extension cells must not move any previously assigned code.
        self.assertEqual(CODEC.encode("кіт", "uk"), (0, 68, 15))  # pinned from origin/master before #31

    def test_the_apostrophe_is_a_sign_not_a_letter(self):
        codes = CODEC.encode("к'у", "uk")
        self.assertEqual(len(codes), 3)
        self.assertEqual(codes[1], geo.sign_code("apostrophe"))


class FailClosedTests(unittest.TestCase):
    def test_unknown_spelling_is_rejected(self):
        with self.assertRaises(UnknownSpelling):
            CODEC.encode("1", "sa-slp1")
        with self.assertRaises(UnknownSpelling):
            CODEC.encode("q1", "uk")

    def test_no_silent_normalisation_of_case(self):
        # SLP1 is case sensitive: `K` (kh) and `k` (k) are different sounds.
        self.assertNotEqual(CODEC.encode("K", "sa-slp1"), CODEC.encode("k", "sa-slp1"))

    def test_reserved_cells_render_only_as_bits(self):
        reserved = [c.code for c in build_cells() if c.status == RESERVED]
        self.assertEqual(len(reserved), 21)
        for code in reserved:
            self.assertEqual(len(CODEC.render([code], "bits")), 7)
            for layout in ("sa-slp1", "uk"):
                with self.assertRaises(UnrenderableCode):
                    CODEC.render([code], layout)

    def test_nasal_vowel_cells_exist_but_slp1_has_no_single_spelling_for_them(self):
        for row in range(7):
            for length in (False, True):
                code = geo.vowel_code(row, nasal=True, length=length)
                with self.assertRaises(UnrenderableCode):
                    CODEC.render([code], "sa-slp1")
        # `aM` is two cells: the vowel a and the anusvara sign.
        self.assertEqual(
            CODEC.encode("aM", "sa-slp1"), (geo.vowel_code(0), geo.sign_code("anusvara"))
        )

    def test_codes_outside_seven_bits_are_rejected(self):
        for code in (-1, 128, 255):
            with self.assertRaises(geo.UPC7GeometryError):
                CODEC.render([code], "bits")
        with self.assertRaises(geo.UPC7GeometryError):
            CODEC.render([True], "bits")

    def test_bits_layout_needs_exact_seven_bit_cells(self):
        for bad in ("101", "10000000", "10a0000"):
            with self.assertRaises(UnknownSpelling):
                CODEC.encode(bad, "bits")


class SignConflictTests(unittest.TestCase):
    """Class 11 has both avagraha and apostrophe, danda and dot: one glyph each,
    so each layout must decide who owns the glyph."""

    def test_sanskrit_owns_apostrophe_and_dot_as_its_own_signs(self):
        self.assertEqual(CODEC.encode("'", "sa-slp1"), (geo.sign_code("avagraha"),))
        self.assertEqual(CODEC.encode(".", "sa-slp1"), (geo.sign_code("danda"),))
        self.assertEqual(CODEC.encode("..", "sa-slp1"), (geo.sign_code("double-danda"),))

    def test_ukrainian_owns_the_ascii_apostrophe_and_dot(self):
        self.assertEqual(CODEC.encode("'", "uk"), (geo.sign_code("apostrophe"),))
        self.assertEqual(CODEC.encode(".", "uk"), (geo.sign_code("dot"),))

    def test_the_same_glyph_is_a_different_code_in_the_two_layouts(self):
        self.assertNotEqual(CODEC.encode("'", "sa-slp1"), CODEC.encode("'", "uk"))
        with self.assertRaises(UnrenderableCode):
            CODEC.render(CODEC.encode("'", "uk"), "sa-slp1")

    def test_parentheses_are_text_codes_here_not_structure(self):
        # UPC-7 has text codes for `(` and `)`. Whether the SENS reader treats
        # them as structure is decided by reader context, not by this table.
        self.assertEqual(CODEC.encode("(", "uk"), (geo.sign_code("left-paren"),))
        self.assertEqual(CODEC.encode(")", "sa-slp1"), (geo.sign_code("right-paren"),))

    def test_operator_glyphs_are_text_codes_never_function_identities(self):
        for glyph, name in (("+", "plus"), ("-", "minus"), ("*", "star"), ("=", "equals")):
            self.assertEqual(CODEC.encode(glyph, "uk"), (geo.sign_code(name),))


class TableFileTests(unittest.TestCase):
    def test_committed_table_is_current(self):
        self.assertTrue(TABLE_PATH.exists(), "run `python3 upc7_table.py --write`")
        self.assertEqual(
            TABLE_PATH.read_text(encoding="utf-8"),
            render_table(),
            "upc7-table.tsv is stale: run `python3 upc7_table.py --write`",
        )

    def test_table_is_deterministic(self):
        self.assertEqual(render_table(), render_table())

    def test_table_rows_agree_with_the_layouts(self):
        lines = TABLE_PATH.read_text(encoding="utf-8").splitlines()
        header, rows = lines[0].split("\t"), lines[1:]
        self.assertEqual(header[:2], ["bits", "hex"])
        self.assertEqual(len(rows), 128)
        for row in rows:
            fields = dict(zip(header, row.split("\t")))
            code = int(fields["bits"], 2)
            self.assertEqual(fields["hex"], f"0x{code:02X}")
            self.assertEqual(unescape(fields["sa-slp1"]), SANSKRIT.code_to_spelling.get(code, ""))
            self.assertEqual(unescape(fields["uk"]), UKRAINIAN.code_to_spelling.get(code, ""))

    def test_the_table_file_has_no_stray_whitespace(self):
        for line in TABLE_PATH.read_text(encoding="utf-8").splitlines():
            self.assertEqual(len(line.split("\t")), 8, line)
            self.assertEqual(line, line.rstrip("\n\r"))


if __name__ == "__main__":
    unittest.main()
