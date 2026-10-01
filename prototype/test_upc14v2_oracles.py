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

import itertools
import unittest

import oracle_io
import upc14v2 as g

S = g.SOUNDS
L = g.LABELS_BY_CODE

LONG_TO_SHORT = {"ā": "a", "ī": "i", "ū": "u", "ṝ": "ṛ", "ḹ": "ḷ"}


def fold(names):
    """Fold the long vowels (vidyut spells them as separate sounds) onto the short ones."""
    return {LONG_TO_SHORT.get(n, n) for n in names}


def read_oracle():
    """(name in Devanagari, start, marker, set of sound names) for each of the 43 pratyaharas."""
    return [(row["name_deva"], row["start_iast"], row["marker_iast"], set(oracle_io.names(row["sounds_iast"])))
            for row in oracle_io.rows("ashtadhyayi-com-pratyahara.tsv")]


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
        self.assertEqual(graph_set("y", "ṇ"), {"y", "v", "r", "l"})


class VidyutTests(unittest.TestCase):
    """Vectors of vidyut's `test_s2` (its pratyahara notation `R2` is the second n)."""

    # (start, marker, nth, the sounds): vidyut's `ac`, `iR2` ... written as start + marker + nth, in IAST.
    S2 = (
        ("a", "c", 1, "a ā i ī u ū ṛ ṝ ḷ ḹ e ai o au"), ("e", "c", 1, "e ai o au"), ("i", "ṇ", 1, "i ī u ū"),
        ("i", "ṇ", 2, "i ī u ū ṛ ṝ ḷ ḹ e ai o au y r l v h"), ("y", "ṇ", 1, "y r l v"),
        ("h", "l", 1, "k kh g gh ṅ c ch j jh ñ ṭ ṭh ḍ ḍh ṇ t th d dh n p ph b bh m y r l v ś ṣ s h"),
        ("ñ", "m", 1, "ṅ ñ ṇ n m"), ("ś", "r", 1, "ś ṣ s"),
    )

    @staticmethod
    def sounds(text):
        return fold(text.split())

    def test_pratyahara_sets_agree_with_vidyuts_test_s2(self):
        for start, marker, nth, expected in self.S2:
            with self.subTest(pratyahara=(start, marker, nth)):
                self.assertEqual(graph_set(start, marker, nth), self.sounds(expected))

    def test_savarna_sets_agree(self):
        # vidyut: a -> a ā, i -> i ī, ku~ -> k kh g gh ṅ, cu~ -> c ch j jh ñ ...
        for short in ("a", "i"):
            self.assertTrue(g.savarna(S[short], g.e_long(S[short])))
        for first, row in (("k", "k kh g gh ṅ"), ("c", "c ch j jh ñ"), ("ṭ", "ṭ ṭh ḍ ḍh ṇ"),
                           ("t", "t th d dh n"), ("p", "p ph b bh m")):
            members = {x for x in S if g.unpack(S[x]).aperture == g.STOP and g.savarna(S[first], S[x])}
            self.assertEqual(members, set(row.split()), first)

    def test_map_jhal_to_jas_agrees_with_all_24_pairs_of_vidyuts_test(self):
        expected = {
            "jh": "j", "bh": "b", "gh": "g", "ḍh": "ḍ", "dh": "d", "j": "j", "b": "b", "g": "g",
            "ḍ": "ḍ", "d": "d", "kh": "g", "ph": "b", "ch": "j", "ṭh": "ḍ", "th": "d", "c": "j",
            "ṭ": "ḍ", "t": "d", "k": "g", "p": "b", "ś": "j", "ṣ": "ḍ", "s": "d", "h": "g",
        }
        jhal = graph_set("jh", "l")
        self.assertEqual(jhal, set(expected))  # vidyut's key set is the same 24 sounds
        jas = [S[x] for x in ("j", "b", "g", "ḍ", "d")]
        for key, want in expected.items():
            with self.subTest(sound=key):
                self.assertEqual(L[g.nearest(S[key], jas)], want)

    def test_map_ku_and_h_to_cu_agrees_with_vidyuts_test(self):
        expected = {"k": "c", "kh": "ch", "g": "j", "gh": "jh", "ṅ": "ñ", "h": "jh"}
        cu = [S[x] for x in ("c", "ch", "j", "jh", "ñ")]
        for key, want in expected.items():
            with self.subTest(sound=key):
                self.assertEqual(L[g.nearest(S[key], cu)], want)


class WhereTheImplementationsDifferTests(unittest.TestCase):
    """Recorded, not hidden: vidyut's own classification differs from this graph's."""

    def test_vidyut_puts_the_sibilants_with_the_semivowels_and_h_with_the_vowels(self):
        # vidyut: Prayatna::Ishat for `yaR` and `Sar`; Vivrta for `ac` and `h`.
        # This graph keeps the sibilants and h on one aperture step (2) between the
        # semivowels (1) and the vowels (3).
        ap = {x: g.unpack(S[x]).aperture for x in ("y", "v", "r", "l", "ś", "ṣ", "s", "h", "a")}
        self.assertEqual({ap[x] for x in ("y", "v", "r", "l")}, {g.SEMIVOWEL})
        self.assertEqual({ap[x] for x in ("ś", "ṣ", "s", "h")}, {g.SIBILANT})
        self.assertEqual(ap["a"], g.VOWEL)

    def test_vidyut_treats_the_sibilants_as_unaspirated_this_graph_as_aspirated(self):
        self.assertEqual({g.unpack(S[x]).asp for x in ("ś", "ṣ", "s")}, {1})


class KasikaSavarnaTests(unittest.TestCase):
    """Closes the gap named in docs/savarna-model-validation-2026-08-30.md (Sakshi, verifier).

    That report checked the older 16-bit vector model against the Kasika on 1.1.9 and found
    it PARTIAL: it folds the four inward efforts into one bit, cannot say that `r` and the
    sibilants have no savarna (`refosmanam savarna na santi`), and can give false positives
    for non-stop sounds. The Kasika lines are quoted there; they were not re-read here.
    """

    def klass(self, letter):
        return {x for x in S if g.savarna(S[letter], S[x])}

    def test_r_and_the_sibilants_have_no_savarna(self):
        for letter in ("r", "ś", "ṣ", "s", "h"):
            self.assertEqual(self.klass(letter), {letter}, letter)

    def test_a_vowel_and_a_consonant_are_never_savarna_1_1_10(self):
        vowels = set(("a", "i", "u", "ṛ", "ḷ", "e", "o", "ai", "au"))
        for x in S:
            for y in S:
                if g.savarna(S[x], S[y]):
                    self.assertEqual(x in vowels, y in vowels, (x, y))

    def test_the_effort_steps_keep_apart_sounds_of_one_place(self):
        # palate: i (vowel) y (semivowel) ś (sibilant) j (stop) share the place, not the effort.
        for a, b in itertools.combinations(("i", "y", "ś", "j"), 2):
            self.assertFalse(g.savarna(S[a], S[b]), (a, b))
        self.assertTrue(g.savarna(S["j"], S["c"]))            # two stops of one varga

    def test_no_false_positive_savarna_among_the_non_stop_consonants(self):
        for a, b in itertools.combinations(("y", "v", "r", "l", "ś", "ṣ", "s", "h"), 2):
            self.assertFalse(g.savarna(S[a], S[b]), (a, b))


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
            for x in ("ś", "ṣ", "s"):
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
