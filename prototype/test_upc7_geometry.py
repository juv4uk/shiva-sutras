#!/usr/bin/env python3
import unittest

from upc7_geometry import (
    CLASS_NAMES,
    CLASS_NONVARGA,
    CLASS_SIGN,
    CLASS_VARGA,
    CLASS_VOWEL,
    CURRENT_UPC8_NONVARGA,
    SIGN_CODE,
    SIGN_NAMES,
    UPC7GeometryError,
    class_of,
    code_bits,
    compress_upc8_nonvarga,
    compress_upc8_vowel,
    decode_varga,
    decode_vowel,
    sign_name,
    varga_code,
    vowel_code,
)


class UPC7GeometryTests(unittest.TestCase):
    def test_classes_partition_all_128_codes(self):
        counts = {cls: 0 for cls in CLASS_NAMES}
        for code in range(128):
            counts[class_of(code)] += 1
            self.assertEqual(len(code_bits(code)), 7)
        self.assertEqual(counts, {
            CLASS_VARGA: 32,
            CLASS_NONVARGA: 32,
            CLASS_VOWEL: 32,
            CLASS_SIGN: 32,
        })

    def test_varga_25_points_are_unique_and_reversible(self):
        codes = []
        for place in range(5):
            for member in range(5):
                code = varga_code(place, member)
                codes.append(code)
                self.assertEqual(class_of(code), CLASS_VARGA)
                self.assertEqual(decode_varga(code), (place, member))
        self.assertEqual(len(codes), 25)
        self.assertEqual(len(set(codes)), 25)

    def test_vowel_28_points_are_unique_and_reversible(self):
        codes = []
        for row in range(7):
            for nasal in (False, True):
                for length in (False, True):
                    code = vowel_code(row, nasal, length)
                    codes.append(code)
                    self.assertEqual(class_of(code), CLASS_VOWEL)
                    self.assertEqual(decode_vowel(code), (row, nasal, length))
        self.assertEqual(len(codes), 28)
        self.assertEqual(len(set(codes)), 28)

    def test_upc8_vowel_compression_drops_only_free_zero_bit(self):
        compressed = []
        for row in range(7):
            for nasal in (0, 1):
                for length in (0, 1):
                    old = 0x80 | (row << 3) | (nasal << 1) | length
                    new = compress_upc8_vowel(old)
                    compressed.append(new)
                    self.assertEqual(
                        new,
                        vowel_code(row, bool(nasal), bool(length)),
                    )
        self.assertEqual(len(set(compressed)), 28)

        with self.assertRaises(UPC7GeometryError):
            compress_upc8_vowel(0x84)  # FREE bit set
        with self.assertRaises(UPC7GeometryError):
            compress_upc8_vowel(0xB8)  # reserved row 7

    def test_current_nonvarga_union_compresses_without_collision(self):
        mapped = {
            old: compress_upc8_nonvarga(old)
            for old in CURRENT_UPC8_NONVARGA
        }
        self.assertEqual(len(mapped), 13)
        self.assertEqual(len(set(mapped.values())), 13)
        self.assertTrue(all(class_of(code) == CLASS_NONVARGA for code in mapped.values()))

    def test_sign_plane_is_fully_named_and_unique(self):
        self.assertEqual(len(SIGN_NAMES), 32)
        self.assertEqual(len(SIGN_CODE), 32)
        self.assertEqual(len(set(SIGN_CODE.values())), 32)
        self.assertEqual(set(SIGN_CODE.values()), set(range(0x60, 0x80)))
        for name, code in SIGN_CODE.items():
            self.assertEqual(class_of(code), CLASS_SIGN)
            self.assertEqual(sign_name(code), name)

    def test_core_lisp_surface_glyphs_have_sign_codes(self):
        for name in (
            "left-paren", "right-paren", "double-quote",
            "apostrophe", "dot", "comma", "backquote",
            "hash", "semicolon",
            "plus", "minus", "star", "slash",
            "equals", "less", "greater", "question",
            "colon",
        ):
            self.assertIn(name, SIGN_CODE)


if __name__ == "__main__":
    unittest.main()
