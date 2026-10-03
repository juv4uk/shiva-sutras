import unittest

import upc14v2 as g
import upc7_linear as X


class LinearCellTests(unittest.TestCase):
    def test_injective_on_the_sanskrit_vertices(self):
        vs = X.vertices()
        self.assertEqual(len(vs), 59)
        self.assertEqual(len({X.image(X.ROWS, c) for c in vs}), 59)
        self.assertTrue(all(0 <= X.image(X.ROWS, c) < 128 for c in vs))

    def test_xor_edges_are_one_delta_for_ANY_matrix_this_is_a_tautology(self):
        import random
        rng = random.Random(7)
        masks = {g.e_asp: 0x1, g.e_voice: 0x2, g.e_long: 0x4}
        vs = set(X.vertices())
        for _ in range(50):
            rows = [rng.getrandbits(14) for _ in range(7)]       # not even injective
            for e, m in masks.items():
                self.assertEqual(X.deltas(rows, e), {X.image(rows, m)})

    def test_nasal_is_not_one_delta(self):
        self.assertEqual(len(X.deltas(X.ROWS, g.e_nasal)), 5)

    def test_injective_matrices_exist_but_are_rare(self):
        found, first = X.search(seed=3, n=20000)
        self.assertGreater(found, 0)
        self.assertLess(found, 20000 // 100)
        self.assertTrue(X.is_injective(first))


if __name__ == "__main__":
    unittest.main()
