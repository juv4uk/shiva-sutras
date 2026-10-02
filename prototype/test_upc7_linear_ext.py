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


if __name__ == "__main__":
    unittest.main()
