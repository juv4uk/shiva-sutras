#!/usr/bin/env python3
"""Every typed edge of the sound graph is one bit operation on the 14-bit code (hypothesis, checked exhaustively)."""

import csv
import os
import unittest

import akshara7
import upc14v2 as g
import upc14v2_bitops as b

HERE = os.path.dirname(__file__)
S = g.SOUNDS


def hand_cells():
    out = {}
    with open(os.path.join(HERE, "upc7-table.tsv"), encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["status"] == "assigned" and row["sa-iast"]:
                out[row["sa-iast"]] = int(row["bits"], 2)
    return out


def edge_pairs(cells, edge):
    return [(cells[p], cells[label]) for label, p, e in g.DERIVATION if e == edge and "+" not in p]


class BitEdgeTests(unittest.TestCase):
    def test_every_edge_equals_its_bit_form_on_every_vertex(self):
        vertices = None
        for name, (n_vertices, equal, _, _) in b.agree_everywhere().items():
            vertices = vertices or n_vertices
            self.assertEqual(equal, n_vertices, name)
        self.assertEqual(vertices, 2232)

    def test_the_bit_forms_fail_closed_on_a_code_that_is_not_a_vertex(self):
        for code in range(1 << g.WIDTH):
            if not b.is_vertex(code):
                for fn in (b.bit_asp, b.bit_voice, b.bit_nasal, b.bit_shift, b.bit_long):
                    with self.assertRaises(g.GraphError):
                        fn(code)

    def test_every_graph_edge_rejects_a_code_that_is_not_a_vertex(self):
        # `e_voice` used to be `c ^ 2` without unpack() and accepted all 14152 non-vertex codes; it validates now.
        leaks = {name: leaks for name, (_, _, _, leaks) in b.agree_everywhere().items()}
        self.assertEqual({k: v for k, v in leaks.items() if v}, {})

    def test_in_the_14_bit_code_asp_voice_and_nasal_are_each_one_constant_flip(self):
        c14 = {n: S[n] for n in S}
        self.assertEqual(b.xor_masks_of_pairs(edge_pairs(c14, "asp")), {0x0001})
        self.assertEqual(b.xor_masks_of_pairs(edge_pairs(c14, "voice")), {0x0002})
        self.assertEqual(b.xor_masks_of_pairs(edge_pairs(c14, "nasal")), {0x0080})

    def test_in_the_7_bit_prototypes_asp_and_voice_are_not_constant_flips(self):
        for name, cells in (("hand table", hand_cells()), ("akshara7", dict(akshara7.SOUND_CODE))):
            self.assertGreater(len(b.xor_masks_of_pairs(edge_pairs(cells, "asp"))), 1, name)
            self.assertGreater(len(b.xor_masks_of_pairs(edge_pairs(cells, "voice"))), 1, name)

    def test_asp_and_voice_commute_on_every_stop(self):
        for code in S.values():
            if g.unpack(code).aperture == g.STOP:
                self.assertEqual(b.bit_asp(b.bit_voice(code)), b.bit_voice(b.bit_asp(code)))

    def test_asp_and_voice_are_involutions(self):
        for code in S.values():
            if g.unpack(code).aperture == g.STOP:
                self.assertEqual(b.bit_asp(b.bit_asp(code)), code)
            self.assertEqual(b.bit_voice(b.bit_voice(code)), code)

    def test_nasal_is_not_an_involution_it_is_one_way(self):
        g_ = S["g"]
        self.assertEqual(b.bit_nasal(b.bit_nasal(g_)), b.bit_nasal(g_))     # idempotent
        self.assertNotEqual(b.bit_nasal(g_), g_)


if __name__ == "__main__":
    unittest.main()
