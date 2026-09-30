#!/usr/bin/env python3
"""Witnesses for the sutra-first 14-bit candidate (shiva-sutras#44)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

import upc14 as u  # noqa: E402
import upc14_bridge as bridge  # noqa: E402
import re  # noqa: E402
import unicodedata  # noqa: E402

KSETRA = os.path.join(os.path.dirname(__file__), "..", "ksetra")
IAST_TO_SLP1 = {unicodedata.normalize("NFC", v): k for k, v in u.IAST.items()}


def nfc(text):
    return unicodedata.normalize("NFC", text)


def read_lines(*parts):
    with open(os.path.join(KSETRA, *parts), encoding="utf-8") as handle:
        return handle.read().splitlines()


def canon_sutras():
    """(text_slp1, it_marker_slp1) per sutra from the encoded canon YAML (no YAML library)."""
    texts, markers = [], []
    for line in read_lines("canon", "siva-sutras-encoded.yaml"):
        m = re.match(r'\s*text_slp1:\s*"([^"]*)"', line)
        if m:
            texts.append(m.group(1))
        m = re.match(r'\s*it_marker_slp1:\s*"([^"]*)"', line)
        if m:
            markers.append(m.group(1))
    return list(zip(texts, markers))


def astadhyayi_pratyaharas():
    """{id: [IAST sounds]} for every pratyahara that lists its set (no YAML library)."""
    out, current, collecting = {}, None, False
    for line in read_lines("astadhyayi", "pratyahara-usage.yaml"):
        m = re.match(r"- id: (\S+)\s*$", line)
        if m:
            current, collecting = m.group(1), False
            continue
        if line.strip() == "set:":
            out[current], collecting = [], True
            continue
        m = re.match(r"  - (\S+)\s*$", line)
        if collecting and m:
            out[current].append(m.group(1))
        elif collecting:
            collecting = False
    return out


def split_pratyahara_id(name):
    """`yaṇ` -> (`y`, `ṇ`, 1); `hal` -> (`h`, `l`, 1); `aṇ2` -> (`a`, `ṇ`, 2); `jhaś` -> (`jh`, `ś`, 1)."""
    name = nfc(name)
    nth = 1
    if name[-1].isdigit():  # `aṇ2`: the second ṇ after the start (sutra 6, not sutra 1)
        nth, name = int(name[-1]), name[:-1]
    marker, prefix = name[-1], name[:-1]
    if len(prefix) > 1 and prefix.endswith("a") and prefix not in ("ai",):
        prefix = prefix[:-1]  # the inherent `a` that carries a consonant
    return IAST_TO_SLP1[prefix], IAST_TO_SLP1[marker], nth


class SutraOrderTests(unittest.TestCase):
    def test_the_sutras_have_57_positions_43_sounds_14_markers(self):
        self.assertEqual(len(u.SUTRAS), 14)
        self.assertEqual(u.RANK_COUNT, 57)
        sounds = [p for p in u.POSITIONS if p.role == u.SOUND]
        markers = [p for p in u.POSITIONS if p.role == u.MARKER]
        self.assertEqual((len(sounds), len(markers)), (43, 14))

    def test_ranks_are_the_recited_order(self):
        self.assertEqual([p.rank for p in u.POSITIONS], list(range(57)))
        self.assertEqual([p.slp1 for p in u.POSITIONS[:4]], ["a", "i", "u", "R"])
        self.assertEqual([p.slp1 for p in u.POSITIONS[-2:]], ["h", "l"])
        self.assertEqual(u.POSITIONS[-1].role, u.MARKER)

    def test_42_distinct_sounds_and_h_occurs_twice(self):
        letters = [p.slp1 for p in u.POSITIONS if p.role == u.SOUND]
        self.assertEqual(len(set(letters)), 42)
        self.assertEqual(letters.count("h"), 2)
        self.assertEqual(len(letters) - len(set(letters)), 1)

    def test_every_it_marker_has_its_own_code_apart_from_the_sound(self):
        # N is the marker of sutra 3 AND the nasal sound of sutra 7; R appears
        # as a marker twice and once as a sound. Role is position.
        for letter in ("N", "R", "Y", "m", "w", "c", "k", "S", "z", "v", "y", "r", "l"):
            ranks = [p.rank for p in u.POSITIONS if p.slp1 == letter]
            roles = {u.POSITIONS[r].role for r in ranks}
            self.assertIn(u.MARKER, roles, letter)
            self.assertEqual(len(ranks), len(set(ranks)))
        self.assertEqual([p.rank for p in u.POSITIONS if p.slp1 == "R"], [3, 19, 23])

    def test_first_sound_rank_uses_the_first_occurrence(self):
        self.assertEqual(u.first_sound_rank("h"), 13)  # sutra 5, not sutra 14
        self.assertEqual(u.first_sound_rank("a"), 0)
        with self.assertRaises(u.UPC14Error):
            u.first_sound_rank("M")  # anusvara is not a sound of the sutras


class PratyaharaTests(unittest.TestCase):
    def test_an_interval_of_ranks_names_the_oracle_cases(self):
        self.assertEqual(set(u.pratyahara_letters("E", "c")), {"E", "O"})          # Ec
        self.assertEqual(set(u.pratyahara_letters("y", "R")), {"y", "v", "r", "l"})  # yaR
        self.assertEqual(set(u.pratyahara_letters("a", "c")), set("aiufxeoEO"))    # ac
        self.assertEqual(set(u.pratyahara_letters("i", "k")), {"i", "u", "f", "x"})  # ik

    def test_marker_rank_disambiguates_the_two_N_markers(self):
        # The first R after `a` is sutra 1's; after `y` it is sutra 6's.
        self.assertEqual(u.marker_rank_after(u.first_sound_rank("a"), "R"), 3)
        self.assertEqual(u.marker_rank_after(u.first_sound_rank("y"), "R"), 19)

    def test_the_sutra_table_equals_the_canonical_yaml(self):
        # The YAML is a separate source of truth; my table is typed from the sutras.
        canon = canon_sutras()
        self.assertEqual(len(canon), 14)
        for mine, (text, marker) in zip(u.SUTRAS, canon):
            self.assertEqual(" ".join(mine), text)
            self.assertEqual(mine[-1], marker)

    # The Astadhyayi YAML is an independent source, but it is not error-free.
    # Three of its 42 entries contradict the canonical oracle
    # (CANONICAL_PRATYAHARA_ORACLE_PASS1.md) or are mis-typed; they are listed
    # here with the reason instead of being silently skipped.
    YAML_DEFECTS = {
        "yaṇ": "lists all 33 consonants from y (that is the set of `yar`); the oracle "
               "and 6.4.81 (iṇo yaṇ) give {y, v, r, l}",
        "has": "typed with plain `s` (no such marker) and lists the whole `hal` set",
        "jhas": "typed with plain `s` (no such marker) and lists the whole `jhal` set",
    }
    # Tradition uses the SECOND ṇ (sutra 6) for `iṇ`. A pratyahara name does not
    # say which occurrence; in rank terms it is just an explicit `nth`.
    NTH_BY_ID = {"iṇ": 2}

    def test_every_classical_pratyahara_agrees_with_the_independent_astadhyayi_yaml(self):
        compared = 0
        for name, sounds in astadhyayi_pratyaharas().items():
            if name in self.YAML_DEFECTS:
                continue
            start, marker, nth = split_pratyahara_id(name)
            nth = self.NTH_BY_ID.get(name, nth)
            theirs = {IAST_TO_SLP1[nfc(s)] for s in sounds}
            mine = set(u.pratyahara_letters(start, marker, nth))
            with self.subTest(pratyahara=name):
                self.assertEqual(mine, theirs)
            compared += 1
        self.assertEqual(compared, 42 - len(self.YAML_DEFECTS))

    def test_the_yaml_defects_are_real_and_yan_matches_the_oracle(self):
        entries = astadhyayi_pratyaharas()
        self.assertEqual(set(self.YAML_DEFECTS) & set(entries), set(self.YAML_DEFECTS))
        yan = {IAST_TO_SLP1[nfc(s)] for s in entries["yaṇ"]}
        self.assertNotEqual(set(u.pratyahara_letters("y", "R")), yan)
        self.assertEqual(set(u.pratyahara_letters("y", "R")), {"y", "v", "r", "l"})  # oracle doc
        for typo in ("has", "jhas"):
            with self.assertRaises(u.UPC14Error):
                u.pratyahara_letters(*split_pratyahara_id(typo)[:2])

    def test_in_rank_terms_in_needs_the_second_marker_not_the_first(self):
        # iṇ = i u ṛ ḷ e o ai au h y v r l (marker of sutra 6); with the first ṇ
        # it would be only {i, u}. The model makes the choice explicit.
        self.assertEqual(set(u.pratyahara_letters("i", "R", 1)), {"i", "u"})
        self.assertEqual(len(u.pratyahara_letters("i", "R", 2)), 13)
        self.assertEqual(u.marker_rank_after(u.first_sound_rank("i"), "R", 2), 19)

    def test_membership_ignores_the_modifiers(self):
        first, end = u.pratyahara_interval("a", "c")
        rank_a = u.first_sound_rank("a")
        plain = u.sutra_code(rank_a)
        long_a = u.sutra_code(rank_a, u.modifiers_of(length=u.LENGTH_LONG))
        nasal = u.sutra_code(rank_a, u.modifiers_of(nasal=True))
        accented = u.sutra_code(rank_a, u.modifiers_of(accent=u.ACCENT_SVARITA))
        for code in (plain, long_a, nasal, accented):
            self.assertTrue(u.in_pratyahara(code, first, end), u.describe(code))

    def test_membership_is_two_comparisons_and_rejects_markers_and_other_kinds(self):
        first, end = u.pratyahara_interval("a", "c")
        marker_inside = u.sutra_code(3)  # the ṇ marker sits between i/u and ṛ
        self.assertFalse(u.in_pratyahara(marker_inside, first, end))
        self.assertFalse(u.in_pratyahara(u.kind_code(u.K_UKRAINIAN, "uk.a"), first, end))
        self.assertFalse(u.in_pratyahara(u.sutra_code(u.first_sound_rank("k")), first, end))

    def test_code_order_is_sutra_order(self):
        codes = [u.sutra_code(r) for r in range(u.RANK_COUNT)]
        self.assertEqual(codes, sorted(codes))


class ValidityTests(unittest.TestCase):
    def test_a_modifier_on_a_consonant_is_invalid(self):
        with self.assertRaises(u.InvalidCode):
            u.validate(u.sutra_code(u.first_sound_rank("k"), u.modifiers_of(nasal=True)))

    def test_a_modifier_on_a_marker_is_invalid(self):
        with self.assertRaises(u.InvalidCode):
            u.validate(u.sutra_code(3, u.modifiers_of(nasal=True)))

    def test_ranks_past_the_last_position_are_invalid(self):
        for rank in range(57, 64):
            with self.assertRaises(u.InvalidCode):
                u.validate(u.make_code(u.K_SUTRA, rank))

    def test_spare_and_reserved_bits_fail_closed(self):
        rank = u.first_sound_rank("a")
        with self.assertRaises(u.InvalidCode):
            u.validate(u.sutra_code(rank, 0b001000))  # spare bit
        with self.assertRaises(u.InvalidCode):
            u.validate(u.sutra_code(rank, 0b000010))  # length 2 is reserved

    def test_e_o_ai_au_are_long_by_nature(self):
        for letter in u.ALWAYS_LONG:
            with self.assertRaises(u.InvalidCode):
                u.validate(u.sutra_code(u.first_sound_rank(letter), u.modifiers_of(length=u.LENGTH_LONG)))
            u.validate(u.sutra_code(u.first_sound_rank(letter), u.modifiers_of(nasal=True)))

    def test_only_the_sutra_kind_has_modifiers(self):
        with self.assertRaises(u.InvalidCode):
            u.validate(u.make_code(u.K_SANSKRIT, 0, 1))

    def test_kind_tables_are_closed(self):
        with self.assertRaises(u.InvalidCode):
            u.validate(u.make_code(u.K_SANSKRIT, len(u.SANSKRIT_SIGNS)))

    def test_the_number_of_defined_cells_is_pinned_and_explained(self):
        consonant_and_marker_cells = 43 - 9 + 14            # plain, no modifiers
        short_long = 5 * (4 * 2 * 2)                        # a i u f x: accent x nasal x length
        long_by_nature = 4 * (4 * 2 * 1)                    # e o ai au
        expected = (
            consonant_and_marker_cells + short_long + long_by_nature
            + len(u.SANSKRIT_SIGNS) + len(u.UKRAINIAN_EXT)
            + len(u.COMMON_SIGNS) + len(u.TEXT_DIGITS)
        )
        codes = u.all_valid_codes()
        self.assertEqual(len(codes), expected)
        self.assertEqual(len(set(codes)), len(codes))
        self.assertLess(len(codes), 1 << 14)  # room to grow, all of it invalid today

    def test_width_is_fourteen_and_two_fill_an_fpga_payload(self):
        self.assertEqual(u.WIDTH * 2, 28)
        self.assertEqual(u.CODE_MAX, 0b11111111111111)
        self.assertEqual(len(u.bits(5)), 14)


class BridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.table = bridge.build_bridge()

    def test_all_107_assigned_upc7_cells_have_a_distinct_valid_upc14_code(self):
        self.assertEqual(len(self.table), 107)
        self.assertEqual(len(set(self.table.values())), 107)  # injective: nothing lost
        for code14 in self.table.values():
            u.validate(code14)

    def test_the_kinds_split_sanskrit_first_then_ukrainian_then_common(self):
        by_kind = {}
        for code14 in self.table.values():
            by_kind[u.split(code14)[0]] = by_kind.get(u.split(code14)[0], 0) + 1
        self.assertEqual(by_kind[u.K_SANSKRIT], 5)
        self.assertEqual(by_kind[u.K_UKRAINIAN], 14)
        self.assertEqual(by_kind[u.K_COMMON], 27)
        self.assertEqual(sum(by_kind.values()), 107)

    def test_ukrainian_letters_that_are_sanskrit_sounds_use_the_sutra_cell(self):
        for word in ("кіт", "ніс", "тут"):
            for code14 in bridge.encode_text(word, "uk"):
                self.assertEqual(u.split(code14)[0], u.K_SUTRA, (word, u.describe(code14)))

    def test_a_ukrainian_word_reaches_all_three_strata(self):
        codes = bridge.encode_text("привіт", "uk")
        kinds = [u.split(c)[0] for c in codes]
        self.assertIn(u.K_SUTRA, kinds)
        self.assertIn(u.K_UKRAINIAN, kinds)  # и is not in the sutras
        # п р (и) в і т : и is the only cell outside the sutras
        self.assertEqual(kinds.count(u.K_UKRAINIAN), 1)

    def test_the_same_sound_has_one_code_across_layouts(self):
        self.assertEqual(bridge.encode_text("kit", "sa-slp1"), bridge.encode_text("кіт", "uk"))

    def test_upc7_e_long_is_ai_in_the_sutras(self):
        # UPC-7 keeps ai as the long form of e; the sutras give it its own position.
        ai = u.sutra_code(u.first_sound_rank("E"))
        self.assertIn(ai, self.table.values())
        self.assertEqual(u.POSITIONS[u.first_sound_rank("E")].sutra, 4)

    def test_sutra_order_is_kept_for_the_sanskrit_sounds(self):
        codes = bridge.encode_text("aiu", "sa-slp1")
        self.assertEqual(list(codes), sorted(codes))


if __name__ == "__main__":
    unittest.main()
