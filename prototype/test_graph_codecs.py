#!/usr/bin/env python3
import unittest

import graph7 as g7
import graph14 as g14

class Graph7Tests(unittest.TestCase):
    def test_seven_bit_nodes_are_unique(self):
        self.assertEqual(len(g7.SOUNDS), 42)
        codes = [g7.code(name) for name in g7.SOUNDS]
        self.assertEqual(len(set(codes)), 42)
        self.assertTrue(all(len(g7.bits(c)) == 7 for c in codes))

    def test_graph_has_typed_edges(self):
        self.assertTrue(g7.neighbors("k", "varga-shift"))
        self.assertIn(g7.node("ai"), g7.neighbors("a", "lift"))
        self.assertTrue(any(edge.kind == "sutra" for edge in g7.EDGES))

    def test_reserved_cells_fail_closed(self):
        with self.assertRaises(g7.InvalidNode):
            g7.validate(42)
        with self.assertRaises(g7.InvalidNode):
            g7.validate(0b1000000)

class Graph14Tests(unittest.TestCase):
    def test_relation_round_trip(self):
        value = g14.encode("k", "c", "varga")
        self.assertEqual(g14.decode(value), ("k", "c", "varga"))
        self.assertEqual(len(g14.bits(value)), 14)

    def test_fourteen_bits_are_source_target_and_kind(self):
        value = g14.encode("a", "ai", "lift")
        self.assertEqual(value >> 8, g14.node("a"))
        self.assertEqual((value >> 2) & 0x3F, g14.node("ai"))
        self.assertEqual(value & 0b11, g14.LIFT)

    def test_reverse_is_explicitly_typed(self):
        value = g14.encode("a", "ai", "lift")
        self.assertEqual(g14.decode(g14.reverse(value)), ("ai", "a", "reverse"))

    def test_invalid_relation_fails_closed(self):
        with self.assertRaises(g14.InvalidRelation):
            g14.encode(42, 0, g14.SUTRA)
        with self.assertRaises(g14.InvalidRelation):
            g14.unpack(1 << 14)

if __name__ == "__main__":
    unittest.main()
