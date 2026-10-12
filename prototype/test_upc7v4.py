#!/usr/bin/env python3
"""Sound7 / UPC-7 v4 falsifiers and exact-width physical codec witnesses.

This is a versioned, explicit English sound-layer projection of UPC14 v3.
No text/orthography, no v2/v3 alias acceptance, no new SENS D7 authority.
"""

import random
import unittest
from pathlib import Path
import csv

import upc14v2 as g
import upc14v3 as v3
import upc7v4 as v4
from upc7_derive import derive

HERE = Path(__file__).resolve().parent


class UPC7V4Witness(unittest.TestCase):
    def test_next_version_is_four_not_an_alias_for_three(self):
        self.assertEqual(v4.VERSION, "UPC-7 v4")
        self.assertEqual(v4.PROFILE, "english-reference-44")
        self.assertEqual(len(v4.candidate_v3_cells()), 124)
        self.assertEqual(v4.ESCAPE, 0b0101111)
        self.assertNotIn(v4.ESCAPE, v4.candidate_v3_cells())
        pinned = list(csv.DictReader(
            (HERE / "upc7-table.tsv").open(encoding="utf-8"), delimiter="\t"))
        old = {int(r["bits"], 2): r for r in pinned
               if r["status"] == "assigned"}
        # The same W7 code was old pinned *l*, not a safe global marker.
        self.assertIn(v4.ESCAPE, old)
        self.assertEqual(old[v4.ESCAPE]["sa-iast"], "l")
        self.assertEqual(len(set(range(128)) - set(old) -
                             set(v4.candidate_v3_cells())), 0)
        # A version header at the transport boundary is mandatory.

    def test_seven_direct_english_plus_37_extensions(self):
        cells = {}
        self.assertEqual(len(v3.ENGLISH), 44)
        self.assertEqual(len(v4.DIRECT_14_TO_7), 42)
        self.assertEqual(len(v4.EXT_CODES14), 37)
        self.assertEqual(len(v4.EXT_RANK), 37)
        self.assertEqual(len({v4.ESCAPE} & set(v4.DIRECT_7_TO_14)), 0)
        self.assertEqual(tuple(sorted(v4.EXT_CODES14)), v4.EXT_CODES14)
        for row in v3.ENGLISH:
            bits = v4.encode_english_tokens((row.ipa,))
            cells[row.ipa] = bits
            expected_length = 1 if row.v2_label else 2
            self.assertEqual(len(bits), expected_length)
            if row.v2_label:
                self.assertEqual(bits, (derive(row.code),))
            else:
                self.assertEqual(bits[0], v4.ESCAPE)
                self.assertEqual(bits[1], v4.EXT_RANK[row.code])
        self.assertEqual(sum(len(cells[t.ipa]) == 1 for t in v3.ENGLISH), 7)
        self.assertEqual(sum(len(cells[t.ipa]) == 2 for t in v3.ENGLISH), 37)

    def test_exact_w14_to_w7_inverse_for_all_42_old_plus_37_new(self):
        admitted = set(g.SOUNDS.values()) | set(v4.EXT_CODES14)
        self.assertEqual(len(admitted), 79)
        for c in admitted:
            with self.subTest(w14=c):
                w7 = v4.encode_sound_codes((c,))
                self.assertEqual(v4.decode_sound_codes(w7), (c,))
                self.assertTrue(all(type(x) is int and 0 <= x < 128
                                    for x in w7))
        for old_label, old14 in g.SOUNDS.items():
            expected = derive(old14)
            self.assertEqual(v4.encode_sound_codes([old14]), (expected,))
            self.assertEqual(v4.candidate_v3_cells()[expected]["sound"],
                             old_label)

    def test_ipa_of_all_44_round_trips_exactly(self):
        for ph in v3.ENGLISH:
            tokens = (ph.ipa,)
            self.assertEqual(v4.decode_english_tokens(
                v4.encode_english_tokens(tokens)), tokens)
        corpus = ("ð", "ə", "ʒ", "t͡ʃ", "æ", "p", "k", "ɡ",
                  "ɪə", "ŋ", "w", "l", "ɔɪ", "d͡ʒ")
        wire = v4.encode_english_tokens(corpus)
        self.assertEqual(v4.decode_english_tokens(wire), corpus)
        packed, count = v4.pack_w7(wire)
        self.assertEqual(v4.unpack_w7(packed, count), wire)
        self.assertEqual(v4.decode_english_tokens(
            v4.unpack_w7(packed, count)), corpus)

    def test_exhaustive_single_cell_admission_and_prefix_truncation(self):
        for c in range(128):
            if c in v4.DIRECT_7_TO_14:
                self.assertEqual(v4.decode_sound_codes([c]),
                                 (v4.DIRECT_7_TO_14[c],))
            else:
                with self.assertRaises(v4.UPC7V4Error):
                    v4.decode_sound_codes([c])

    def test_exhaustive_prefix_and_payload_gate(self):
        for rank in range(128):
            seq = (v4.ESCAPE, rank)
            if rank < 37:
                expected = v4.EXT_CODES14[rank]
                self.assertEqual(v4.decode_sound_codes(seq), (expected,))
                self.assertEqual(v4.encode_sound_codes((expected,)), seq)
            else:
                with self.assertRaises(v4.UPC7V4Error):
                    v4.decode_sound_codes(seq)
        for bad in (-1, 128, 256, True, None, "0", 0.25):
            with self.assertRaises(v4.UPC7V4Error):
                v4.decode_sound_codes((v4.ESCAPE, bad))

    def test_all_44_squared_sequences_have_unique_parse(self):
        phones = tuple(ph.ipa for ph in v3.ENGLISH)
        encodings = {}
        for a in phones:
            for b in phones:
                sequence = (a, b)
                w7 = v4.encode_english_tokens(sequence)
                self.assertEqual(v4.decode_english_tokens(w7), sequence)
                self.assertNotIn(w7, encodings)
                encodings[w7] = sequence
        self.assertEqual(len(encodings), 44 * 44)

    def test_explicit_version_bound_frame_not_legacy_auto_decode(self):
        sample = ("θ", "ə", "m", "t͡ʃ", "ɹ", "iː")
        frame = v4.encode_english_frame(sample)
        self.assertEqual(frame.version, "UPC-7 v4")
        self.assertEqual(frame.profile, "english-reference-44")
        self.assertEqual(v4.decode_english_frame(frame), sample)
        for bad in (
            v4.UPC7V4Frame("UPC-7 v3", frame.profile,
                           frame.cell_count, frame.payload),
            v4.UPC7V4Frame(frame.version, "uk", frame.cell_count,
                           frame.payload),
            (frame.payload, frame.cell_count),
            None,
        ):
            with self.subTest(bad=bad), self.assertRaises(v4.UPC7V4Error):
                v4.decode_english_frame(bad)

    def test_bitaligned_pack_no_hidden_cell_padding(self):
        self.assertEqual(v4.pack_w7(())[0], b"")
        rng = random.Random(140704)
        pool = tuple(g.SOUNDS.values()) + v4.EXT_CODES14
        for n in range(66):
            codes = tuple(rng.choice(pool) for _ in range(n))
            cells = v4.encode_sound_codes(codes)
            packed, count = v4.pack_w7(cells)
            self.assertEqual(count, len(cells))
            self.assertEqual(len(packed), (7 * count + 7) // 8)
            self.assertEqual(v4.unpack_w7(packed, count), cells)
            self.assertEqual(v4.decode_sound_codes(
                v4.unpack_w7(packed, count)), codes)
        for n in range(1, 12):
            data, size = v4.pack_w7([0] * n)
            pad = (-(7 * n)) % 8
            if pad:
                mutated = data[:-1] + bytes([data[-1] | 1])
                with self.assertRaises(v4.UPC7V4Error):
                    v4.unpack_w7(mutated, size)
        with self.assertRaises(v4.UPC7V4Error):
            v4.unpack_w7(b"\x00\x00", 1)

    def test_non_sound_text_cells_and_version_misuse_fail_closed(self):
        from upc7_geometry import sign_code
        for glyph in ("space", "dot", "left-paren", "right-paren"):
            # The phoneme-only decoder must not turn a text sign into sound.
            cell = sign_code(glyph)
            with self.subTest(sign=glyph), self.assertRaises(v4.UPC7V4Error):
                v4.decode_sound_codes([cell])
        for nonsound in (None, "text", False, 128, -1, 0x4000):
            with self.assertRaises(v4.UPC7V4Error):
                v4.encode_sound_codes([nonsound])
        for fake_ipa in ("th", "sh", "word", "tʃ", "дж", "я", "g", "y"):
            with self.assertRaises(v3.UPC14V3Error):
                v4.encode_english_tokens((fake_ipa,))

    def test_physical_cost_is_seven_bits_or_fourteen_bits(self):
        for row in v3.ENGLISH:
            count = len(v4.encode_english_tokens([row.ipa]))
            self.assertEqual(7 * count, 7 if row.v2_label else 14)
        cost = sum(7 * len(v4.encode_english_tokens((row.ipa,)))
                   for row in v3.ENGLISH)
        self.assertEqual(cost, 7 * 7 + 37 * 14)  # 567 vs 616 uncompressed W14
        self.assertEqual(44 * 14 - cost, 49)

    def test_bit_flip_mutation_does_not_produce_silent_near_equivalence(self):
        for row in v3.ENGLISH:
            cells = v4.encode_english_tokens([row.ipa])
            self.assertEqual(v4.decode_sound_codes(cells), (row.code,))
            if len(cells) == 2:
                # An unknown extension rank, not a plausible nearest phone.
                with self.assertRaises(v4.UPC7V4Error):
                    v4.decode_sound_codes((v4.ESCAPE, 127))


if __name__ == "__main__":
    unittest.main()
