#!/usr/bin/env python3
"""Named pratyahara (shiva-sutras#44): the name -> (start, marker, nth, occurrence) table of upc14v2."""

import unittest

import oracle_io
import upc14v2 as g

S, L = g.SOUNDS, g.LABELS_BY_CODE


def named_set(name):
    return {L[c] for c in g.pratyahara_named(name)}


class NamedPratyaharaTests(unittest.TestCase):
    def test_every_row_gives_the_set_of_the_plain_pratyahara_call(self):
        for name, (start, marker, nth, occurrence) in g.NAMED_PRATYAHARA.items():
            with self.subTest(name=name):
                self.assertEqual(g.pratyahara_named(name),
                                 g.pratyahara(S[start], marker, nth, start_occurrence=occurrence))

    def test_the_43_names_of_the_oracle_agree(self):
        """ashtadhyayi.com: each of its 43 rows (the name aṇ occurs twice: 6.3.111 and 1.1.69) equals the named set."""
        rows = oracle_io.rows("ashtadhyayi-com-pratyahara.tsv")
        self.assertEqual(len(rows), 43)
        for row in rows:
            name, sounds = row["name_iast"], set(oracle_io.names(row["sounds_iast"]))
            with self.subTest(name=name):
                candidates = [name] + (["aṇ2"] if name == "aṇ" else [])
                self.assertTrue(any(named_set(n) == sounds for n in candidates), (name, sorted(sounds)))

    def test_the_names_the_oracle_does_not_have_are_checked_by_hand(self):
        self.assertEqual(named_set("ñam"), {"ñ", "m", "ṅ", "ṇ", "n"})            # ञमन्ताड्डः (Kasika preface)
        self.assertEqual(named_set("aṇ2"), {"a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au", "h", "y", "v", "r", "l"})

    def test_the_repeated_markers_follow_the_kasika(self):
        """aṇ the first ṇ, iṇ the second (txt 99-103); aṇ2 (1.1.69) the second ṇ; ṅam is not ñam."""
        self.assertEqual(named_set("aṇ"), {"a", "i", "u"})
        self.assertEqual(named_set("iṇ"), {"i", "u", "ṛ", "ḷ", "e", "o", "ai", "au", "h", "y", "v", "r", "l"})
        self.assertEqual(named_set("ṅam"), {"ṅ", "ṇ", "n"})
        self.assertNotEqual(named_set("ṅam"), named_set("ñam"))

    def test_bhas_is_bhaṣ_and_there_is_no_bhaś(self):
        self.assertEqual(named_set("bhaṣ"), {"bh", "gh", "ḍh", "dh"})
        self.assertNotIn("bhaś", g.NAMED_PRATYAHARA)

    def test_h_starts_take_the_first_recitation(self):
        self.assertEqual(g.NAMED_PRATYAHARA["hal"][3], 1)
        self.assertEqual(g.NAMED_PRATYAHARA["haś"][3], 1)

    def test_an_unknown_name_raises_graph_error_and_nfc_is_applied(self):
        with self.assertRaises(g.GraphError):
            g.pratyahara_named("xyz")
        self.assertEqual(g.pratyahara_named("aṇ"), g.pratyahara_named("aṇ"))         # ṇ composed or not
        self.assertEqual(g.pratyahara_named("ṇ".join(["a", ""]).replace("ṇ", "ṇ")), g.pratyahara_named("aṇ"))

    def test_there_are_43_names_and_each_marker_letter_exists_on_the_path(self):
        self.assertEqual(len(g.NAMED_PRATYAHARA), 43)
        markers = {n.label for n in g.PATH if n.is_marker}
        for name, (start, marker, nth, occurrence) in g.NAMED_PRATYAHARA.items():
            self.assertIn(marker, markers, name)


if __name__ == "__main__":
    unittest.main()
