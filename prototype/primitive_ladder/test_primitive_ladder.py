import unittest

from primitive_ladder import Primitive, compose


class PrimitiveLadderTests(unittest.TestCase):
    def test_lift_preserves_value(self):
        atom = Primitive("x", 8, 0xAB).lift(16)
        self.assertEqual(atom.value, 0xAB)
        self.assertEqual(atom.width, 16)

    def test_compose_packs_two_bytes(self):
        pair = compose(Primitive("a", 8, 0x12), Primitive("b", 8, 0x34), 16)
        self.assertEqual(pair.value, 0x1234)

    def test_overflow_is_rejected(self):
        with self.assertRaises(ValueError):
            Primitive("x", 8, 0x100)

    def test_narrow_compose_is_rejected(self):
        with self.assertRaises(ValueError):
            compose(Primitive("a", 8, 1), Primitive("b", 8, 2), 8)


if __name__ == "__main__":
    unittest.main()
