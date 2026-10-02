import unittest

import upc7_digits_compare as D


class DigitCandidateTests(unittest.TestCase):
    def test_free_cells(self):
        self.assertEqual(len(D.free_v3()), 21)
        self.assertEqual(len(D.free_pinned()), 21)
        self.assertEqual(D.free_pinned()[:10], [25, 26, 27, 28, 29, 30, 31, 33, 34, 35])
        self.assertEqual(D.free_v3()[:10], [25, 26, 27, 28, 29, 30, 31, 34, 35, 41])

    def test_the_affine_candidates_give_the_digit_by_bit_operations_the_ordinal_ones_do_not(self):
        c = D.candidates()
        self.assertEqual(D.affine_decoder(c["affine-v3"]), [(4, 0), (3, 1), (8, 1), (5, 1)])
        self.assertIsNotNone(D.affine_decoder(c["affine-pinned"]))
        self.assertIsNone(D.affine_decoder(c["ordinal-v3"]))
        self.assertIsNone(D.affine_decoder(c["ordinal-pinned"]))

    def test_class_counts(self):
        m = {k: D.metrics(v) for k, v in D.candidates().items()}
        self.assertEqual((m["affine-v3"]["varga"], m["affine-v3"]["non-varga"]), (6, 4))
        self.assertEqual((m["affine-pinned"]["varga"], m["affine-pinned"]["non-varga"]), (6, 4))
        self.assertEqual((m["ordinal-v3"]["varga"], m["ordinal-v3"]["non-varga"]), (7, 3))
        self.assertEqual((m["ordinal-pinned"]["varga"], m["ordinal-pinned"]["non-varga"]), (7, 3))

    def test_only_affine_v3_collides_with_the_pinned_table(self):
        m = {k: D.metrics(v)["collides_with_pinned"] for k, v in D.candidates().items()}
        self.assertEqual(m["affine-v3"], [52])           # the pinned cell of h; v3 moved h, so v3 needs the h/r/l migration
        self.assertEqual(m["ordinal-v3"], [])
        self.assertEqual(m["ordinal-pinned"], [])
        self.assertEqual(m["affine-pinned"], [])

    def test_the_pinned_table_is_unchanged(self):
        import hashlib
        import os
        raw = open(os.path.join(D.HERE, "upc7-table.tsv"), "rb").read()
        want = open(os.path.join(D.HERE, "upc7-table.sha256")).read().split()[0]
        self.assertEqual(hashlib.sha256(raw).hexdigest(), want)


if __name__ == "__main__":
    unittest.main()
