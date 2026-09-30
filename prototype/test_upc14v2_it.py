#!/usr/bin/env python3
"""it-samjna on the sutra path (shiva-sutras#44). Kasika readings are the shiva agent's,
kAshikAvRRitti.txt line numbers as reported; quotes are marked (q), inferences (i)."""

import unittest

import upc14v2 as g

S = g.SOUNDS
L = g.LABELS_BY_CODE


class ItTests(unittest.TestCase):
    def test_the_it_nodes_are_the_last_hal_of_each_of_the_14_sutras(self):
        ranks = g.it_ranks()
        self.assertEqual(len(ranks), 14)
        lasts = []
        rank = -1
        for sutra in g.SUTRAS:
            rank += len(sutra)
            lasts.append(rank)
        self.assertEqual(list(ranks), lasts)

    def test_all_14_are_consonants_hal(self):
        hal = {L[c] for c in g.pratyahara(S["h"], "l")}                    # hal: h..l, 1.3.3 `halantyam`
        for rank in g.it_ranks():
            self.assertIn(g.PATH[rank].label, hal, g.PATH[rank])

    def test_the_marker_letters_in_recitation_order(self):
        # (q) 1.3.3 names the first four: ṇ k ṅ c (line 3349); (i) the other ten follow the same rule.
        self.assertEqual("".join(g.PATH[r].label for r in g.it_ranks()), "RkNcwRmYzSvyrl")

    def test_1_1_71_the_pratyahara_has_its_own_first_sound_and_what_is_between_not_the_marker(self):
        # (q) line 1647: the first with the it-final one denotes the letters fallen between them
        # and its own form; the it itself is not a member (it is `it`, 1.3.3, and disappears, 1.3.9).
        for start, marker, marker_as_sound in (("a", "c", "c"), ("a", "R", "R"), ("i", "k", "k"), ("y", "R", "R")):
            members = g.pratyahara(S[start], marker)
            self.assertIn(S[start], members, (start, marker))              # its own form
            self.assertNotIn(S[marker_as_sound], members, (start, marker)) # the marker's letter is a different node

    def test_the_second_n_and_the_second_h_are_resolved_by_occurrence_not_by_the_kasika(self):
        # (i) the Kasika says nothing about which occurrence 1.1.71 takes; the graph uses the
        # ksetra/astadhyayi/occurrence-resolution.yaml tradition (an = first n, in = second n).
        self.assertEqual(len(g.pratyahara(S["a"], "R", 1)), 3)
        self.assertEqual(len(g.pratyahara(S["i"], "R", 2)), 13)
        self.assertEqual(len(g.start_ranks(S["h"])), 2)

    def test_a_marker_is_a_meta_cell_and_never_a_sound_vertex(self):
        for rank in g.it_ranks():
            with self.assertRaises(g.InvalidCode):
                g.unpack(g.meta_code(rank))                               # 1.3.9: it disappears
        for rank in range(len(g.PATH)):
            if not g.is_it(rank):
                with self.assertRaises(g.InvalidCode):
                    g.meta_code(rank)


if __name__ == "__main__":
    unittest.main()
