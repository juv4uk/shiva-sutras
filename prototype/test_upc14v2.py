#!/usr/bin/env python3
"""Witnesses for the graph canon UPC-14 v2 (shiva-sutras#44)."""

import itertools
import os
import random
import re
import unicodedata
import unittest

import upc14v2 as g

HERE = os.path.dirname(__file__)
KSETRA = os.path.join(HERE, "..", "ksetra")
S = g.SOUNDS
L = g.LABELS_BY_CODE

# SLP1 -> IAST: only to read the independent YAML sources. Not part of the code.
IAST = {
    "a": "a", "i": "i", "u": "u", "f": "ṛ", "x": "ḷ", "e": "e", "o": "o", "E": "ai", "O": "au",
    "h": "h", "y": "y", "v": "v", "r": "r", "l": "l", "Y": "ñ", "m": "m", "N": "ṅ", "R": "ṇ",
    "n": "n", "J": "jh", "B": "bh", "G": "gh", "Q": "ḍh", "D": "dh", "j": "j", "b": "b",
    "g": "g", "q": "ḍ", "d": "d", "K": "kh", "P": "ph", "C": "ch", "W": "ṭh", "T": "th",
    "c": "c", "w": "ṭ", "t": "t", "k": "k", "p": "p", "S": "ś", "z": "ṣ", "s": "s",
}
FROM_IAST = {unicodedata.normalize("NFC", v): k for k, v in IAST.items()}


def nfc(text):
    return unicodedata.normalize("NFC", text)


def read_lines(*parts):
    with open(os.path.join(KSETRA, *parts), encoding="utf-8") as handle:
        return handle.read().splitlines()


def canon_sutras():
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
    out, current, collecting = {}, None, False
    for line in read_lines("astadhyayi", "pratyahara-usage.yaml"):
        m = re.match(r"- id: (\S+)\s*$", line)
        if m:
            current, collecting = nfc(m.group(1)), False
            continue
        if line.strip() == "set:":
            out[current], collecting = [], True
            continue
        m = re.match(r"  - (\S+)\s*$", line)
        if collecting and m:
            out[current].append(FROM_IAST[nfc(m.group(1))])
        elif collecting:
            collecting = False
    return out


def split_id(name):
    """`yaṇ` -> (`y`, `ṇ`, 1); `aṇ2` -> (`a`, `ṇ`, 2); `jhaś` -> (`jh`, `ś`, 1)."""
    nth = 1
    if name[-1].isdigit():
        nth, name = int(name[-1]), name[:-1]
    marker, prefix = name[-1], name[:-1]
    if len(prefix) > 1 and prefix.endswith("a") and prefix != "ai":
        prefix = prefix[:-1]
    return FROM_IAST[prefix], FROM_IAST[marker], nth


class LayoutTests(unittest.TestCase):
    def test_fourteen_bits_and_two_fill_an_fpga_payload(self):
        self.assertEqual(g.WIDTH, 14)
        self.assertEqual(2 * g.WIDTH, 28)  # fpga-lisp: 32-bit word = 4 tag + 28 value

    def test_the_42_sounds_have_42_distinct_valid_codes(self):
        self.assertEqual(len(S), 42)
        self.assertEqual(len(set(S.values())), 42)
        for code in S.values():
            self.assertLess(code, 1 << 14)
            g.unpack(code)

    def test_the_fields_are_the_coordinates(self):
        v = g.unpack(S["g"])
        self.assertEqual((v.place, v.aperture, v.voice, v.asp, v.nasal, v.length), (g.K, 0, 1, 0, 0, 0))
        v = g.unpack(S["h"])  # lift of gh: throat, sibilant row, voiced, aspirated
        self.assertEqual((v.place, v.aperture, v.voice, v.asp), (g.K, g.SIBILANT, 1, 1))
        v = g.unpack(S["v"])  # semivowel with two places: teeth and lips
        self.assertEqual((v.place, v.aperture), (g.D | g.O, g.SEMIVOWEL))

    def test_ill_formed_codes_fail_closed(self):
        with self.assertRaises(g.InvalidCode):
            g.unpack(g.make(0, g.STOP))                      # no articulator
        with self.assertRaises(g.InvalidCode):
            g.unpack(g.make(g.K, 5))                         # off the aperture path
        with self.assertRaises(g.InvalidCode):
            g.unpack(g.make(g.K, g.VOWEL, length=3))         # off the length path
        with self.assertRaises(g.InvalidCode):
            g.unpack(g.make(g.K, g.STOP, length=1))          # a consonant has no length
        with self.assertRaises(g.InvalidCode):
            g.unpack(g.meta_code(3))                         # a marker is not a sound
        with self.assertRaises(g.InvalidCode):
            g.unpack(1 << 14)

    def test_this_module_is_not_bound_to_sanskrit_or_ukrainian_layers(self):
        with open(os.path.join(HERE, "upc14v2.py"), encoding="utf-8") as handle:
            source = handle.read()
        for forbidden in ("import upc7", "from upc7", "import upc14 ", "from upc14 ", "devanagari", "cyrillic"):
            self.assertNotIn(forbidden, source.lower())


class DerivationTests(unittest.TestCase):
    def test_42_sounds_are_reached_from_one_seed_by_41_edges(self):
        self.assertEqual(len(g.DERIVATION), 41)
        children = [child for child, _, _ in g.DERIVATION]
        self.assertEqual(len(set(children)), 41)
        self.assertEqual(set(children) | {g.SEED[0]}, set(S))

    def test_the_derivation_is_a_tree_in_topological_order(self):
        reached = {g.SEED[0]}
        for child, parent, _edge in g.DERIVATION:
            for one in parent.split("+"):
                self.assertIn(one, reached, f"{child} uses {one} before it exists")
            reached.add(child)

    def test_only_e_o_and_v_need_more_than_one_edge(self):
        composite = {c for c, p, e in g.DERIVATION if "+" in p or "+" in e}
        self.assertEqual(composite, {"e", "o", "v"})

    def test_each_sound_is_the_result_of_replaying_its_edge(self):
        edges = {"asp": g.e_asp, "voice": g.e_voice, "nasal": g.e_nasal, "shift": g.e_shift,
                 "lift1": lambda c: g.e_lift(c, 1), "lift2": lambda c: g.e_lift(c, 2),
                 "lift3": lambda c: g.e_lift(c, 3)}
        for child, parent, edge in g.DERIVATION:
            if edge in edges:
                self.assertEqual(edges[edge](S[parent]), S[child], child)

    def test_dot_export_has_every_sound_and_every_edge(self):
        dot = g.to_dot()
        self.assertEqual(dot.count("tooltip"), 42)
        self.assertGreaterEqual(dot.count("->"), 41)


class StructureTests(unittest.TestCase):
    ROWS = {"k": "kKgGN", "c": "cCjJY", "w": "wWqQR", "t": "tTdDn", "p": "pPbBm"}

    def test_shift_commutes_with_every_row_edge_so_the_five_vargas_are_isomorphic(self):
        # The 25 varga sounds are a 5 x 5 grid graph: (place spine) x (row of members).
        rows = list(self.ROWS.values())
        for a, b in zip(rows, rows[1:]):
            for x, y in zip(a, b):
                self.assertEqual(g.e_shift(S[x]), S[y], (x, y))
        for row in rows:
            k, kh, gg, gh, ng = (S[x] for x in row)
            self.assertEqual((g.e_asp(k), g.e_voice(k), g.e_asp(gg), g.e_nasal(gg)), (kh, gg, gh, ng))
        for edge in (g.e_asp, g.e_voice, g.e_nasal):
            for row in rows[:-1]:
                for x in row:
                    try:
                        left = g.e_shift(edge(S[x]))
                    except g.GraphError:
                        continue
                    self.assertEqual(left, edge(g.e_shift(S[x])), (edge.__name__, x))

    def test_aperture_is_a_path_lifts_compose(self):
        for a in range(0, 3):
            for b in range(0, 3 - a):
                base = S["j"]
                self.assertEqual(g.e_lift(g.e_lift(base, a), b), g.e_lift(base, a + b))
        self.assertEqual(g.e_lift(S["y"], 2), S["i"])     # semivowel -> vowel, same place
        self.assertEqual(g.e_lift(S["j"], 1), S["y"])
        with self.assertRaises(g.GraphError):
            g.e_lift(S["E"], 1)                            # the path ends

    def test_v_is_u_with_teeth_added_at_semivowel_aperture(self):
        vu, vv = g.unpack(S["u"]), g.unpack(S["v"])
        self.assertEqual(vv.place, vu.place | g.D)
        self.assertEqual((vu.aperture, vv.aperture), (g.VOWEL, g.SEMIVOWEL))

    def test_the_edges_out_of_k_and_g_are_the_expected_ones(self):
        self.assertEqual(g.neighbors(S["k"]), {"asp": S["K"], "voice": S["g"], "nasal": S["N"], "shift": S["c"]})   # nasal: k -> the varga nasal
        self.assertEqual(g.neighbors(S["g"]),
                         {"asp": S["G"], "voice": S["k"], "nasal": S["N"], "shift": S["j"]})


class SutraPathTests(unittest.TestCase):
    def test_the_path_has_57_nodes_43_sounds_14_markers(self):
        self.assertEqual(len(g.PATH), 57)
        self.assertEqual(sum(1 for n in g.PATH if n.is_marker), 14)
        self.assertEqual(sum(1 for n in g.PATH if not n.is_marker), 43)
        self.assertEqual([n.rank for n in g.PATH], list(range(57)))

    def test_the_sutra_text_equals_the_canonical_yaml(self):
        canon = canon_sutras()
        self.assertEqual(len(canon), 14)
        for mine, (text, marker) in zip(g.SUTRAS, canon):
            self.assertEqual(" ".join(mine), text)
            self.assertEqual(mine[-1], marker)

    def test_h_occurs_twice_on_the_path_but_is_one_vertex(self):
        ranks = [n.rank for n in g.PATH if not n.is_marker and n.label == "h"]
        self.assertEqual(ranks, [13, 55])
        self.assertEqual(g.first_rank(S["h"]), 13)

    def test_a_marker_is_a_meta_cell_that_names_its_place(self):
        self.assertEqual(g.meta_code(3) >> 13, 1)
        with self.assertRaises(g.InvalidCode):
            g.meta_code(0)  # a sound, not a marker


class PratyaharaTests(unittest.TestCase):
    YAML_DEFECTS = {"yaṇ", "has", "jhas"}   # wrong in the YAML; see UPC14 v1 tests and the doc
    NTH = {"iṇ": 2}

    def letters(self, start, marker, nth=1):
        return {L[c] for c in g.pratyahara(S[start], marker, nth)}

    def test_39_of_42_classical_pratyaharas_agree_with_the_independent_yaml(self):
        compared = 0
        for name, sounds in astadhyayi_pratyaharas().items():
            if name in self.YAML_DEFECTS:
                continue
            start, marker, nth = split_id(name)
            nth = self.NTH.get(name, nth)
            with self.subTest(name=name):
                self.assertEqual(self.letters(start, marker, nth), set(sounds))
            compared += 1
        self.assertEqual(compared, 39)

    def test_the_oracle_case_yan_is_y_v_r_l(self):
        self.assertEqual(self.letters("y", "R"), {"y", "v", "r", "l"})
        self.assertEqual(self.letters("E", "c"), {"E", "O"})


class GrammarQueryTests(unittest.TestCase):
    def test_savarna_is_equal_place_and_aperture(self):
        a, aa = S["a"], g.e_long(S["a"])
        self.assertTrue(g.savarna(a, aa))                       # short and long
        nasal = g.Vertex(g.K, 1, g.VOWEL, 0, 1, 0).code
        self.assertTrue(g.savarna(a, nasal))                    # the nose is separate
        self.assertFalse(g.savarna(S["a"], S["i"]))
        self.assertTrue(all(g.savarna(S["k"], S[x]) for x in "KgGN"))  # a whole varga row incl. the nasal
        self.assertFalse(g.savarna(S["k"], S["c"]))

    def test_dirgha_merges_savarna_simple_vowels(self):
        for x in "aiuf":
            long_form = g.dirgha(S[x], S[x])
            self.assertEqual(g.unpack(long_form).length, g.LONG)
            self.assertEqual(g.unpack(long_form).place, g.unpack(S[x]).place)
        with self.assertRaises(g.GraphError):
            g.dirgha(S["x"], S["x"])          # the Kasika (389): ḷ has no long form
        with self.assertRaises(g.GraphError):
            g.dirgha(S["a"], S["i"])

    def test_guna_and_vrddhi_are_place_join_with_an_aperture_lift(self):
        self.assertEqual(g.guna(S["a"], S["i"]), S["e"])
        self.assertEqual(g.guna(S["a"], S["u"]), S["o"])
        self.assertEqual(g.vrddhi(S["a"], S["e"]), S["E"])
        self.assertEqual(g.vrddhi(S["a"], S["o"]), S["O"])
        self.assertEqual(g.vrddhi(S["a"], S["E"]), S["E"])

    def test_yan_substitution_is_the_nearest_semivowel_and_is_not_definitional(self):
        # iko yan aci: i u ri li -> y v r l. Nothing in the derivation says so; the
        # nearest vertex of {y v r l} in the place lattice does (1.1.50).
        yan = [S[x] for x in "yvrl"]
        self.assertEqual({x: L[g.nearest(S[x], yan)] for x in "iufx"},
                         {"i": "y", "u": "v", "f": "r", "x": "l"})
        # u sits on the lips; v has teeth AND lips, so it is nearer than y, r or l.
        def apart(x, y):
            return bin(g.unpack(S[x]).place ^ g.unpack(S[y]).place).count("1")

        for other in "yrl":
            self.assertGreater(apart("u", other), apart("u", "v"))

    def test_jas_substitution_is_the_nearest_voiced_unaspirated_stop_of_the_same_varga(self):
        jas = [S[x] for x in "jbgqd"]
        rows = {"kKgGN": "g", "cCjJY": "j", "wWqQR": "q", "tTdDn": "d", "pPbBm": "b"}
        for row, expected in rows.items():
            for x in row[:4]:                           # the stops of the varga (not the nasal)
                self.assertEqual(L[g.nearest(S[x], jas)], expected, x)

    def test_a_tie_is_not_resolved(self):
        # e has the throat AND the palate: a and i are equally near it.
        with self.assertRaises(g.Ambiguous):
            g.nearest(S["e"], [S["a"], S["i"]])


class NaturalClassTests(unittest.TestCase):
    """Experiment: how many natural feature classes are intervals in the sutra order?"""

    ATOMS = (
        [(f"place has {n}", lambda v, b=b: bool(v.place & b)) for n, b in zip("KTMDO", (g.K, g.T, g.M, g.D, g.O))]
        + [("nasal", lambda v: v.nasal == 1), ("not nasal", lambda v: v.nasal == 0)]
        + [(f"aperture {a}", lambda v, a=a: v.aperture == a) for a in range(5)]
        + [("aperture <= 2", lambda v: v.aperture <= 2), ("aperture >= 3", lambda v: v.aperture >= 3)]
        + [("voiced", lambda v: v.voice == 1), ("unvoiced", lambda v: v.voice == 0),
           ("aspirated", lambda v: v.asp == 1), ("unaspirated", lambda v: v.asp == 0),
           ("long", lambda v: v.length >= 1), ("short", lambda v: v.length == 0)]
    )

    @classmethod
    def setUpClass(cls):
        vertices = {label: g.unpack(code) for label, code in S.items()}
        cls.classes = {}
        for size in (1, 2, 3):
            for combo in itertools.combinations(cls.ATOMS, size):
                members = frozenset(l for l, v in vertices.items() if all(p(v) for _, p in combo))
                if members and members not in cls.classes:
                    cls.classes[members] = [name for name, _ in combo]
        cls.sutra_order = [n.label for n in g.PATH if not n.is_marker]

    @staticmethod
    def is_interval(members, order):
        return any(frozenset(order[i:j + 1]) == members
                   for i in range(len(order)) for j in range(i, len(order)))

    def count(self, order):
        return sum(1 for members in self.classes if self.is_interval(members, order))

    def test_195_distinct_natural_classes_and_54_are_intervals_in_sutra_order(self):
        self.assertEqual(len(self.classes), 195)
        self.assertEqual(self.count(self.sutra_order), 54)

    def test_the_sutra_order_beats_every_one_of_50_random_orders(self):
        rng = random.Random(14)
        labels = list(S)
        best = 0
        for _ in range(50):
            order = labels[:]
            rng.shuffle(order)
            best = max(best, self.count(order))
        self.assertLess(best, 54)
        self.assertLessEqual(best, 40)

    def test_aperture_and_voice_are_intervals_but_no_single_place_is(self):
        by_name = {tuple(names): members for members, names in self.classes.items() if len(names) == 1}
        for name in [f"aperture {a}" for a in range(5)] + ["voiced", "unvoiced", "nasal", "long"]:
            self.assertTrue(self.is_interval(by_name[(name,)], self.sutra_order), name)
        for name in ("K", "T", "M", "D", "O"):
            self.assertFalse(self.is_interval(by_name[(f"place has {name}",)], self.sutra_order), name)


if __name__ == "__main__":
    unittest.main()
