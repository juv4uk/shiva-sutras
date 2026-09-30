#!/usr/bin/env python3
"""Consonant sandhi as graph queries: witnesses (shiva-sutras#44)."""

import csv
import os
import unittest

import upc14v2 as g
import upc14v2_sandhi as sd

HERE = os.path.dirname(__file__)
S = g.SOUNDS
L = g.LABELS_BY_CODE
VOWELS = set("aAiIuUfFxXeEoO")


def labels(codes):
    return {L[c] for c in codes}


def oracle(name):
    path = os.path.join(HERE, "oracles", name)
    with open(path, encoding="utf-8") as handle:
        lines = [line for line in handle if not line.startswith("#")]
    return list(csv.DictReader(lines, delimiter="\t"))


class ClassTests(unittest.TestCase):
    """Every class is computed from the graph, and equals the classical one."""

    def test_pratyahara_classes_computed_from_the_path(self):
        self.assertEqual(labels(sd.JAS), set("jbgqd"))
        self.assertEqual(labels(sd.JHAS), set("JBGQDjbgqd"))
        self.assertEqual(labels(sd.NAM), set("YmNRn"))
        self.assertEqual(labels(sd.CAR), set("cwtkpSzs"))
        self.assertEqual(labels(sd.KHAR), set("KPCWTcwtkpSzs"))
        self.assertEqual(len(sd.JHAL), 24)
        self.assertEqual(len(sd.YAR), 32)
        self.assertEqual(len(sd.AT), 13)

    def test_savarna_classes_are_the_five_vargas_with_the_nasal(self):
        self.assertEqual(labels(sd.KU), set("kKgGN"))
        self.assertEqual(labels(sd.CU), set("cCjJY"))
        self.assertEqual(labels(sd.WU), set("wWqQR"))
        self.assertEqual(labels(sd.TU), set("tTdDn"))
        self.assertEqual(labels(sd.PU), set("pPbBm"))
        self.assertEqual(labels(sd.SCU), set("cCjJYS"))
        self.assertEqual(labels(sd.STU), set("wWqQRz"))


class RuleTests(unittest.TestCase):
    def test_each_rule_fires_alone_and_leaves_a_trace(self):
        self.assertEqual(sd.final_stop("t", "a").sutras, ("8.2.39",))
        self.assertEqual(sd.final_stop("t", "a").left, "d")
        r = sd.final_stop("t", "c")            # tat + ca -> tac ca
        self.assertEqual((r.left, r.right), ("c", "c"))
        self.assertEqual(r.sutras, ("8.2.39", "8.4.40", "8.4.55"))   # t -> d -> j -> c
        r = sd.final_stop("t", "w")            # tat + ṭa -> taṭ ṭa
        self.assertEqual((r.left, r.right), ("w", "w"))
        self.assertEqual(r.sutras, ("8.2.39", "8.4.41", "8.4.55"))   # t -> d -> q -> w
        r = sd.final_stop("k", "n")            # vak + na -> vaṅ na
        self.assertEqual((r.left, r.right, r.sutras), ("N", "n", ("8.2.39", "8.4.45")))
        r = sd.final_stop("k", "h")            # vak + ha -> vag gha
        self.assertEqual((r.left, r.right, r.sutras), ("g", "G", ("8.2.39", "8.4.62")))
        r = sd.final_stop("t", "S")            # tat + śa -> tac cha
        self.assertEqual((r.left, r.right), ("c", "C"))
        self.assertIn("8.4.63", r.sutras)
        r = sd.final_stop("t", "l")            # tat + la -> tal la
        self.assertEqual((r.left, r.right), ("l", "l"))

    def test_voiceless_stops_stay_voiceless_before_voiceless_and_voice_before_voiced(self):
        self.assertEqual(sd.final_stop("t", "k").left, "t")     # devoicing restores it (8.4.55)
        self.assertIn("8.4.55", sd.final_stop("t", "k").sutras)
        self.assertEqual(sd.final_stop("t", "g").left, "d")
        self.assertEqual(sd.final_stop("p", "b").left, "b")

    def test_the_place_rules_are_the_nearest_vertex_of_a_graph_computed_set(self):
        # s and t-varga become palatal before a palatal: nothing but place distance says so.
        self.assertEqual({L[g.nearest(S[x], sd.SCU)] for x in "sTdD"} , {"S", "C", "j", "J"})


class VidyutOracleTests(unittest.TestCase):
    """99 rows of vidyut's generated external-sandhi rules for a final k, ṭ, p or t."""

    # Two rows where the implementations disagree because they order rules differently.
    ORDER_DEPENDENT = {("t", "Y"): "n Y", ("t", "R"): "n R"}

    def test_the_fixture_is_the_99_rows(self):
        self.assertEqual(len(oracle("vidyut-sandhi-final-stops.tsv")), 99)

    def test_the_graph_reproduces_97_of_99(self):
        agree, differ = 0, []
        for row in oracle("vidyut-sandhi-final-stops.tsv"):
            first, second, result = row["first_slp1"], row["second_slp1"], row["result_slp1"]
            got = sd.final_stop(first, second)
            mine = f"{got.left} {got.right}"
            if mine == result:
                agree += 1
            else:
                differ.append((first, second, result, mine))
        self.assertEqual(agree, 97, differ)
        self.assertEqual({(f, s): r for f, s, r, _ in differ}, self.ORDER_DEPENDENT)

    def test_the_two_disagreements_are_a_rule_order_choice_not_a_bug(self):
        # t + ñ: ascending sutra order gives ñ ñ (8.4.40 then 8.4.45); vidyut gives n ñ.
        r = sd.final_stop("t", "Y")
        self.assertEqual((r.left, r.right, r.sutras), ("Y", "Y", ("8.2.39", "8.4.40", "8.4.45")))


class CoqOracleTests(unittest.TestCase):
    """Maps parsed from the Coq formalization `paninian-verified` (definitions as written)."""

    @staticmethod
    def coq(rule):
        return {row["input_slp1"]: row["output_slp1"] for row in oracle("paninian-verified-consonant-maps.tsv")
                if row["rule"] == rule}

    def test_palatalization_and_retroflexion_equal_the_nearest_vertex(self):
        for rule, targets in (("8.4.40", sd.SCU), ("8.4.41", sd.STU)):
            table = self.coq(rule)
            self.assertEqual(len(table), 6)
            for key, want in table.items():
                self.assertEqual(L[g.nearest(S[key], targets)], want, (rule, key))

    def test_devoicing_agrees(self):
        table = self.coq("8.4.55")
        self.assertEqual(len(table), 10)
        for key, want in table.items():
            self.assertEqual(L[g.nearest(S[key], sd.CAR)], want, key)

    def test_voicing_of_aspirates_is_where_the_coq_definition_departs_from_the_sutra(self):
        # 8.4.53 says jhal -> jas, and jas = j b g ḍ d has NO aspirate. The Coq
        # `voiced_of` maps kh -> gh (keeping the aspiration); the sutra as written
        # (and vidyut, and this graph) give kh -> g.
        table = self.coq("8.4.53")
        self.assertEqual(table["K"], "G")
        self.assertEqual(L[g.nearest(S["K"], sd.JAS)], "g")
        differing = {k for k, v in table.items() if L[g.nearest(S[k], sd.JAS)] != v}
        self.assertEqual(differing, {"K", "C", "W", "T", "P"})   # exactly the five aspirates
        for k in set(table) - differing:
            self.assertEqual(L[g.nearest(S[k], sd.JAS)], table[k])


class ContactTests(unittest.TestCase):
    """8.4.40-44 in both directions; examples tabulated from the Kasika by the shiva agent
    (kAshikAvRRitti.txt lines 83644-83760; second-hand, not re-read here)."""

    def pair(self, left, right, **kw):
        r = sd.contact(left, right, **kw)
        return r.left + r.right

    def test_the_dental_changes_before_a_palatal_or_retroflex(self):
        self.assertEqual(self.pair("s", "S"), "SS")        # vrksas sete
        self.assertEqual(self.pair("s", "c"), "Sc")        # vrksas cinoti
        self.assertEqual(self.pair("t", "C"), "cC")        # agnicic chadayati
        self.assertEqual(self.pair("t", "c"), "cc")        # agnicic cinoti
        self.assertEqual(self.pair("s", "z"), "zz")        # vrksas sande
        self.assertEqual(self.pair("d", "q"), "qq")        # agnicid dinah
        self.assertEqual(self.pair("d", "Q"), "qQ")        # agnicid dhaukate

    def test_and_after_a_palatal_or_retroflex_which_the_left_only_version_missed(self):
        self.assertEqual(self.pair("j", "n"), "jY")        # yajnah  (yaj + nah: n -> ñ)
        self.assertEqual(self.pair("c", "n"), "cY")        # yacna
        self.assertEqual(self.pair("z", "t"), "zw")        # pesta
        self.assertEqual(self.pair("z", "T"), "zW")        # krsistha
        self.assertEqual(self.pair("s", "j"), "Sj")        # intermediate only: masj -> maśj -> majj (other sutras finish it)

    def test_the_blocks(self):
        r = sd.contact("S", "n")                           # prasnah, visnah
        self.assertEqual((r.left, r.right, r.blocked), ("S", "n", ("8.4.44",)))
        self.assertEqual(sd.contact("S", "t").right, "t")
        r = sd.contact("t", "z")                           # agnicitsande, bhavansande
        self.assertEqual((r.left, r.right, r.blocked), ("t", "z", ("8.4.43",)))
        self.assertEqual(sd.contact("n", "z").left, "n")
        r = sd.contact("w", "s", padanta=True)             # svalit saye
        self.assertEqual((r.left, r.right, r.blocked), ("w", "s", ("8.4.42",)))
        self.assertEqual(sd.contact("w", "t", padanta=True).right, "t")   # madhulit tarati

    def test_inside_a_word_the_same_pair_is_not_blocked_by_8_4_42(self):
        self.assertEqual(self.pair("w", "s"), "wz")

    def test_torli_n_plus_l_gives_the_nasal_l(self):
        # Kasika 8.4.60: bhavaml lunati (a nasal l); t + l gives the oral l
        r = sd.final_stop("n", "l")
        self.assertEqual((r.left, r.sutras), ("l~", ("8.4.60",)))
        self.assertEqual(sd.final_stop("t", "l").left, "l")

    def test_the_trace_names_the_sutra_and_the_direction(self):
        r = sd.contact("j", "n")
        self.assertEqual([(s.sutra, s.before, s.after) for s in r.trace], [("8.4.40", "n", "Y")])
        r = sd.contact("t", "c")
        self.assertEqual([(s.sutra, s.before, s.after) for s in r.trace], [("8.4.40", "t", "c")])


class DomainTests(unittest.TestCase):
    """No rule may call `nearest` outside its domain (review by the shiva agent)."""

    def test_no_rule_raises_ambiguous_for_any_pair_of_sounds(self):
        import upc14v2_vowel_sandhi as vs
        labels = list(S) + list("AIUFX")
        for a in labels:
            for b in labels:
                for fn in (sd.final_stop, sd.contact, vs.vowel_sandhi):
                    with self.subTest(rule=fn.__name__, pair=a + b):
                        fn(a, b)                                     # must not raise

    def test_a_semivowel_before_a_nasal_becomes_its_own_nasal_form(self):
        # v has two places (teeth, lips): no varga nasal is nearest to it, so 8.4.45 nasalises v itself.
        r = sd.final_stop("v", "n")
        self.assertEqual((r.left, r.sutras), ("v~", ("8.4.45",)))
        self.assertEqual(sd.final_stop("y", "m").left, "y~")
        self.assertEqual(sd.final_stop("l", "n").left, "l~")

    def test_r_has_no_nasal_form_so_8_4_45_leaves_it_alone(self):
        # Kasika line 391: y v l have a nasal and a non-nasal form, r has not. The y v l nasal
        # forms are an inference from 391 (the examples of 8.4.45 are all stops).
        r = sd.final_stop("r", "n")
        self.assertEqual((r.left, r.sutras), ("r", ()))

    def test_nearest_is_ambiguous_for_sounds_outside_the_domain_of_yan(self):
        for x in "kKgGNha":
            with self.subTest(source=x):
                with self.assertRaises(g.Ambiguous):
                    g.nearest(S[x], sd.YAN)


class NatvaTests(unittest.TestCase):
    def word(self, text):
        return tuple(text)

    def test_a_word_final_n_is_not_changed_8_4_37(self):
        # Kasika 8.4.37 (line 83569, via the shiva agent): vrksan, plaksan, arin, girin
        for word in ("vfkzAn", "plakzAn", "arIn", "girIn"):
            with self.subTest(word=word):
                self.assertEqual("".join(sd.natva(tuple(word))), word)
        # a stem that is not a whole pada still gets natva at its end
        self.assertEqual("".join(sd.natva(tuple("purAn"), complete_pada=False)), "purAR")

    def test_natva_words(self):
        # SLP1: rAmeRa (ramena -> ramena?) see each case
        cases = {
            "rAmena": "rAmeRa",      # rāmeṇa: r ā m e n a, through ā m e
            "kfzRa": "kfzRa",        # already ṇ after ṣ
            "varna": "varRa",        # varṇa: n right after r
            "puRAna": "puRAna",      # (no n) control
            "purAna": "purARa",      # purāṇa
            "brAhmana": "brAhmaRa",  # brāhmaṇa: through ā h m a
            "arjuna": "arjuna",      # j (a palatal) blocks
            "arthana": "arthana",    # th (a dental) blocks
            "kfSAnu": "kfSAnu",      # ś is neither aṭ, ku nor pu: it blocks
            "nara": "nara",          # n is first: no trigger before it
        }
        for text, want in cases.items():
            with self.subTest(word=text):
                self.assertEqual("".join(sd.natva(self.word(text))), want)

    def test_the_four_examples_of_the_coq_file(self):
        # natva_ex1..4 of paninian.v: [r a] n -> ṇ ; [a i] n -> n ; [r t a] n -> n ; [ṣ a] n -> ṇ
        for before, want in (("ra", "R"), ("ai", "n"), ("rta", "n"), ("za", "R")):
            with self.subTest(before=before):
                self.assertEqual(sd.natva(tuple(before + "n"), complete_pada=False)[-1], want)   # context test, not a whole pada

    def test_the_through_set_is_at_ku_pu_computed_from_the_graph(self):
        self.assertEqual(len(sd.AT), 13)
        self.assertEqual(labels(sd.NATVA_THROUGH) & set("SzslcwtT"), set())

    def test_coq_blocker_list_lets_a_sibilant_through_and_the_graph_query_does_not(self):
        # Coq `is_natva_blocker` lists palatals, retroflexes, dentals and l; the
        # sibilants s' s. s are NOT in it (source-confirmed, Coq not run), so for
        # kṛśānu it would return ṇ. Pāṇini's own set (aṭ, ku, pu) excludes ś, and the
        # graph-computed set keeps n.
        self.assertEqual("".join(sd.natva(tuple("kfSAnu"))), "kfSAnu")


if __name__ == "__main__":
    unittest.main()
