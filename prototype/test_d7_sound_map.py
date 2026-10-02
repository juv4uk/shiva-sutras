import unittest

import d7_sound_map as M


class D7SoundMapTests(unittest.TestCase):
    def test_counts_come_from_the_artifacts(self):
        n, extra, reached = M.graph_counts()
        self.assertEqual((n, extra, reached), (42, 17, 17))

    def test_the_coordinate_laws_die_under_relabelling(self):
        for key, (pairs, add, xor, ident) in M.attack(trials=300).items():
            self.assertEqual(pairs, 10)
            self.assertTrue(ident[0])                      # the control: on the unpermuted cells the additive delta IS constant
            self.assertLess(add, 0.01)
            self.assertLess(xor, 0.01)

    def test_rows_have_the_d7_columns(self):
        rows = M.rows()
        self.assertTrue(all(len(r) == len(M.COLUMNS) for r in rows))
        self.assertEqual([r for r in rows if r[0].startswith("decimal digits")][0][1], "Text (NOT Number)")


if __name__ == "__main__":
    unittest.main()
