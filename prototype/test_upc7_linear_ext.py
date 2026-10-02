import unittest

import upc14v2 as g
import upc7_linear as X
import upc7_linear_ext as E


class NasalTests(unittest.TestCase):
    def test_the_nasal_masks(self):
        self.assertEqual(E.nasal_masks(), {0x82: 5, 0x83: 5, 0x80: 18, 0x81: 5, 0x0: 18})

    def test_four_nonzero_deltas_for_every_injective_matrix_so_one_is_impossible(self):
        for rows in ([*X.ROWS], [*E.SHIFT_ROWS]):
            self.assertTrue(X.is_injective(rows))
            nonzero = X.deltas(rows, g.e_nasal) - {0}
            self.assertEqual(len(nonzero), 4)


class ClassTests(unittest.TestCase):
    def test_only_nonvarga_patterns_are_affine(self):
        affine = {p for p, (_, a) in E.class_patterns().items() if a}
        self.assertEqual(affine, {(0, 0, 0), (0, 1, 0), (1, 0, 1), (1, 1, 1)})
        self.assertFalse(E.class_patterns()[(1, 0, 0)][1])      # is_stop
        self.assertFalse(E.class_patterns()[(0, 0, 1)][1])      # is_vowel

    def test_stops_need_more_classes_than_the_quotient_has(self):
        places, classes = E.stop_quotient_classes()
        self.assertEqual(places, 5)
        self.assertEqual(classes, 4)
        self.assertGreater(places, classes)


class ShiftTests(unittest.TestCase):
    def test_a_found_matrix_is_injective_and_intertwines_shift_affinely_not_linearly(self):
        rows = E.SHIFT_ROWS
        self.assertTrue(X.is_injective(rows))
        pairs = E.edge_pairs(g.e_shift)
        self.assertEqual(len(pairs), 36)
        self.assertTrue(E.affine_T_exists(rows, pairs))
        self.assertFalse(E.affine_T_exists(rows, pairs, linear=True))


class GuardedXorTests(unittest.TestCase):
    def test_nasal_join_long_are_a_xor_with_a_mask_fixed_by_the_guard_class_on_all_2232_vertices(self):
        vs = E.all_vertices()
        self.assertEqual(len(vs), 2232)
        for c in vs:
            self.assertEqual(g.e_nasal(c), c ^ E.nasal_mask(c))
            for atoms in (g.K, g.T, g.M, g.D, g.O, g.K | g.T, g.K | g.O):
                self.assertEqual(g.e_join(c, atoms), c ^ E.join_mask(c, atoms))
            try:
                after = g.e_long(c)
            except g.GraphError:
                continue
            self.assertEqual(after, c ^ E.long_mask(c))

    def test_number_of_masks_per_edge_over_all_vertices(self):
        self.assertEqual(E.edge_mask_count(g.e_asp), (248, 1, 1984))
        self.assertEqual(E.edge_mask_count(g.e_voice), (2232, 1, 0))
        self.assertEqual(E.edge_mask_count(g.e_nasal), (2232, 8, 0))
        self.assertEqual(E.edge_mask_count(g.e_long), (1488, 3, 744))
        self.assertEqual(E.edge_mask_count(g.e_shift), (1080, 15, 1152))
        self.assertEqual(E.edge_mask_count(lambda c: g.e_join(c, g.K)), (2232, 2, 0))

    def test_the_shift_matrix_does_not_extend_to_all_shift_pairs(self):
        full = [(c, g.e_shift(c)) for c in E.all_vertices() if not g.unpack(c).place & g.O]
        self.assertEqual(len(full), 1080)
        self.assertFalse(E.affine_T_exists(E.SHIFT_ROWS, full))


if __name__ == "__main__":
    unittest.main()
