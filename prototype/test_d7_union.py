import random
import unittest

import d7_union as U


class D7UnionTests(unittest.TestCase):
    def test_L1_eq_is_total_and_cross_type_is_false(self):
        self.assertEqual(U.eq(U.Sound7(59), U.Sound7(59)), 1)
        self.assertEqual(U.eq(U.Number(59), U.Number(59)), 1)
        self.assertEqual(U.eq(U.Sound7(59), U.Number(59)), 0)      # same bits, different type
        self.assertEqual(U.eq(U.Number(59), U.Sound7(59)), 0)

    def test_L2_mixed_or_sound_operations_raise(self):
        s, n = U.Sound7(3), U.Number(3)
        for f in (U.add, U.mul, U.lt):
            for a, b in ((s, n), (n, s), (s, s)):
                with self.assertRaises(U.D7TypeError):
                    f(a, b)
        self.assertEqual(U.add(n, U.Number(2)).q, 5)

    def test_L3_relabelling_sound_cells_changes_no_number_result(self):
        rng = random.Random(3)
        nums = [U.Number(x) for x in (0, 1, 7, 59, 127, 128, "1/3")]
        before = [(U.add(a, b).q, U.mul(a, b).q, U.lt(a, b), U.eq(a, b)) for a in nums for b in nums]
        for _ in range(50):
            perm = list(range(128))
            rng.shuffle(perm)
            relabelled = [U.Sound7(perm[c]) for c in range(128)]          # any relabelling of the sound cells
            self.assertEqual(len(relabelled), 128)
            after = [(U.add(a, b).q, U.mul(a, b).q, U.lt(a, b), U.eq(a, b)) for a in nums for b in nums]
            self.assertEqual(before, after)

    def test_L3_a_seven_bit_number_is_not_the_sound_with_the_same_bits(self):
        for v in range(128):
            self.assertEqual(U.eq(U.Number(v), U.Sound7(v)), 0)

    def test_L4_no_implicit_conversion_and_the_projection_is_a_string(self):
        w = U.sound_to_wire(U.Sound7(0x3B))
        self.assertEqual(w, "#t7:3b")
        self.assertIsInstance(w, str)
        with self.assertRaises(U.D7TypeError):
            U.sound_to_wire(U.Number(59))
        with self.assertRaises(U.D7TypeError):
            U.Sound7(128)
        with self.assertRaises(U.D7TypeError):
            U.Sound7(True)


if __name__ == "__main__":
    unittest.main()
