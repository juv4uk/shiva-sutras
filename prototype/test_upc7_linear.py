import unittest

import upc14v2 as g
import upc7_linear as X


class LinearCellTests(unittest.TestCase):
    def test_injective_on_the_sanskrit_vertices(self):
        vs = X.vertices()
        self.assertEqual(len(vs), 59)
        self.assertEqual(len({X.image(X.ROWS, c) for c in vs}), 59)
        self.assertTrue(all(0 <= X.image(X.ROWS, c) < 128 for c in vs))

    def test_xor_edges_are_one_delta(self):
        for e in (g.e_asp, g.e_voice, g.e_long):
            self.assertEqual(len(X.deltas(X.ROWS, e)), 1, e.__name__)

    def test_nasal_is_not_one_delta(self):
        self.assertEqual(len(X.deltas(X.ROWS, g.e_nasal)), 5)


if __name__ == "__main__":
    unittest.main()
