#!/usr/bin/env python3
"""External oracles for the graph canon UPC-14 v2 (shiva-sutras#44).

Two implementations written by others, neither of which this code has seen:

* ashtadhyayi.com data: 43 pratyaharas as (name, set of sounds), committed as
  facts in `oracles/ashtadhyayi-com-pratyahara.tsv` (provenance in its header).
* vidyut (ambuda-org, MIT), `vidyut-prakriya/src/sounds.rs` at commit
  8da2f90bee3ce1c07505fa432fc3729e3f7e02ea: the vectors of its own unit tests
  `test_s2`, `test_map_sounds_jhal_jhash`, `test_map_sounds_kuh_cu`, copied here
  as data with that attribution. Vidyut spells long vowels as separate sounds;
  this graph treats length as a coordinate, so vidyut's long forms are folded
  onto the short vowel before comparing.
"""

import os
import unittest

import upc14v2 as g

HERE = os.path.dirname(__file__)
S = g.SOUNDS
L = g.LABELS_BY_CODE

LONG_TO_SHORT = {"A": "a", "I": "i", "U": "u", "F": "f", "X": "x"}


def fold(letters):
    return {LONG_TO_SHORT.get(c, c) for c in letters}


def read_oracle():
    rows = []
    with open(os.path.join(HERE, "oracles", "ashtadhyayi-com-pratyahara.tsv"), encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#") or line.startswith("name_devanagari") or not line.strip():
                continue
            name, start, marker, sounds = line.rstrip("\n").split("\t")
            rows.append((name, start, marker, set(sounds)))
    return rows


def graph_set(start, marker, nth=1):
    return {L[c] for c in g.pratyahara(S[start], marker, nth)}


class AshtadhyayiComTests(unittest.TestCase):
    def test_all_43_phonetic_pratyaharas_are_an_interval_of_the_path(self):
        rows = read_oracle()
        self.assertEqual(len(rows), 43)
        used = {}
        for name, start, marker, sounds in rows:
            found = None
            for nth in (1, 2):
                try:
                    if graph_set(start, marker, nth) == sounds:
                        found = nth
                        break
                except g.GraphError:
                    continue
            with self.subTest(name=name):
                self.assertIsNotNone(found, f"{name}: no occurrence of the marker gives {sorted(sounds)}")
            used.setdefault(name, []).append(found)
        # `an` is listed twice upstream (sutra 1 and sutra 6), and `in` uses the second n.
        self.assertEqual(sorted(used["अण्"]), [1, 2])
        self.assertEqual(used["इण्"], [2])

    def test_yan_here_agrees_with_the_oracle_document_and_disagrees_with_the_ksetra_yaml(self):
        names = {name: sounds for name, _, _, sounds in read_oracle()}
        self.assertEqual(names["यण्"], {"y", "v", "r", "l"})
        self.assertEqual(graph_set("y", "R"), {"y", "v", "r", "l"})


class VidyutTests(unittest.TestCase):
    """Vectors of vidyut's `test_s2` (its pratyahara notation `R2` is the second n)."""

    S2 = (
        ("ac", "aAiIuUfFxXeEoO"), ("ec", "eEoO"), ("iR", "iIuU"),
        ("iR2", "iIuUfFxXeEoOyrlvh"), ("yaR", "yrlv"),
        ("hal", "kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"), ("Yam", "NYRnm"), ("Sar", "Szs"),
    )

    @staticmethod
    def parse(name):
        second = name.endswith("2")
        name = name[:-1] if second else name
        return name[0], name[-1], 2 if second else 1

    def test_pratyahara_sets_agree_with_vidyuts_test_s2(self):
        for name, expected in self.S2:
            start, marker, nth = self.parse(name)
            with self.subTest(pratyahara=name):
                self.assertEqual(graph_set(start, marker, nth), fold(expected))

    def test_savarna_sets_agree(self):
        # vidyut: a -> aA, i -> iI, ku~ -> kKgGN, cu~ -> cCjJY
        for short, expected in (("a", "a"), ("i", "i")):
            self.assertTrue(g.savarna(S[short], g.e_long(S[short])))
        for first, row in (("k", "kKgGN"), ("c", "cCjJY"), ("w", "wWqQR"), ("t", "tTdDn"), ("p", "pPbBm")):
            members = {x for x in S if g.unpack(S[x]).aperture == g.STOP and g.savarna(S[first], S[x])}
            self.assertEqual(members, set(row), first)

    def test_map_jhal_to_jas_agrees_with_all_24_pairs_of_vidyuts_test(self):
        expected = {
            "J": "j", "B": "b", "G": "g", "Q": "q", "D": "d", "j": "j", "b": "b", "g": "g",
            "q": "q", "d": "d", "K": "g", "P": "b", "C": "j", "W": "q", "T": "d", "c": "j",
            "w": "q", "t": "d", "k": "g", "p": "b", "S": "j", "z": "q", "s": "d", "h": "g",
        }
        jhal = graph_set("J", "l")
        self.assertEqual(jhal, set(expected))  # vidyut's key set is the same 24 sounds
        jas = [S[x] for x in "jbgqd"]
        for key, want in expected.items():
            with self.subTest(sound=key):
                self.assertEqual(L[g.nearest(S[key], jas)], want)

    def test_map_ku_and_h_to_cu_agrees_with_vidyuts_test(self):
        expected = {"k": "c", "K": "C", "g": "j", "G": "J", "N": "Y", "h": "J"}
        cu = [S[x] for x in "cCjJY"]
        for key, want in expected.items():
            with self.subTest(sound=key):
                self.assertEqual(L[g.nearest(S[key], cu)], want)


class WhereTheImplementationsDifferTests(unittest.TestCase):
    """Recorded, not hidden: vidyut's own classification differs from this graph's."""

    def test_vidyut_puts_the_sibilants_with_the_semivowels_and_h_with_the_vowels(self):
        # vidyut: Prayatna::Ishat for `yaR` and `Sar`; Vivrta for `ac` and `h`.
        # This graph keeps the sibilants and h on one aperture step (2) between the
        # semivowels (1) and the vowels (3).
        ap = {x: g.unpack(S[x]).aperture for x in "yvrlSzsha"}
        self.assertEqual({ap[x] for x in "yvrl"}, {g.SEMIVOWEL})
        self.assertEqual({ap[x] for x in "Szsh"}, {g.SIBILANT})
        self.assertEqual(ap["a"], g.VOWEL)

    def test_vidyut_treats_the_sibilants_as_unaspirated_this_graph_as_aspirated(self):
        self.assertEqual({g.unpack(S[x]).asp for x in "Szs"}, {1})


class SensitivityTests(unittest.TestCase):
    """The interval result must not be an artifact of this graph's own feature choices."""

    def counts(self, changes):
        from test_upc14v2 import NaturalClassTests as N

        N.setUpClass()
        vertices = {l: g.unpack(c) for l, c in S.items()}
        for label, code in changes.items():
            vertices[label] = g.unpack(code)
        classes = {}
        for size in (1, 2, 3):
            import itertools
            for combo in itertools.combinations(N.ATOMS, size):
                members = frozenset(l for l, v in vertices.items() if all(p(v) for _, p in combo))
                if members and members not in classes:
                    classes[members] = 1
        return sum(1 for m in classes if N.is_interval(m, N.sutra_order))

    def test_the_54_survives_vidyuts_classification_of_the_sibilants_and_h(self):
        def sib(asp, ap):
            out = {}
            for x in "Szs":
                v = g.unpack(S[x])
                out[x] = g.make(v.place, ap, voice=v.voice, asp=asp)
            return out

        unaspirated = sib(0, g.SIBILANT)                              # vidyut: alpaprana
        vidyut = sib(0, g.SEMIVOWEL)                                   # + ishat with the semivowels
        h = g.unpack(S["h"])
        vidyut["h"] = g.make(h.place, g.VOWEL, voice=1, asp=1)         # + vivrta with the vowels
        results = (self.counts({}), self.counts(unaspirated), self.counts(vidyut))
        self.assertEqual(results, (54, 55, 54))
        for value in results:
            self.assertGreater(value, 40)                              # random orders stay <= 40


if __name__ == "__main__":
    unittest.main()
