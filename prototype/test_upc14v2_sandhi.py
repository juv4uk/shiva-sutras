#!/usr/bin/env python3
"""Consonant sandhi as graph queries: witnesses (shiva-sutras#44)."""

import os
import unittest

import oracle_io
import upc14v2 as g
import upc14v2_sandhi as sd

HERE = os.path.dirname(__file__)
S = g.SOUNDS
L = g.LABELS_BY_CODE
VOWELS = set(("a", "ā", "i", "ī", "u", "ū", "ṛ", "ṝ", "ḷ", "ḹ", "e", "ai", "o", "au"))


def labels(codes):
    return {L[c] for c in codes}


def oracle(name):
    return oracle_io.rows(name)


class ClassTests(unittest.TestCase):
    """Every class is computed from the graph, and equals the classical one."""

    def test_pratyahara_classes_computed_from_the_path(self):
        self.assertEqual(labels(sd.JAS), set(("j", "b", "g", "ḍ", "d")))
        self.assertEqual(labels(sd.JHAS), set(("jh", "bh", "gh", "ḍh", "dh", "j", "b", "g", "ḍ", "d")))
        self.assertEqual(labels(sd.NAM), set(("ñ", "m", "ṅ", "ṇ", "n")))
        self.assertEqual(labels(sd.CAR), set(("c", "ṭ", "t", "k", "p", "ś", "ṣ", "s")))
        self.assertEqual(labels(sd.KHAR), set(("kh", "ph", "ch", "ṭh", "th", "c", "ṭ", "t", "k", "p", "ś", "ṣ", "s")))
        self.assertEqual(len(sd.JHAL), 24)
        self.assertEqual(len(sd.YAR), 32)
        self.assertEqual(len(sd.AT), 13)

    def test_savarna_classes_are_the_five_vargas_with_the_nasal(self):
        self.assertEqual(labels(sd.KU), set(("k", "kh", "g", "gh", "ṅ")))
        self.assertEqual(labels(sd.CU), set(("c", "ch", "j", "jh", "ñ")))
        self.assertEqual(labels(sd.WU), set(("ṭ", "ṭh", "ḍ", "ḍh", "ṇ")))
        self.assertEqual(labels(sd.TU), set(("t", "th", "d", "dh", "n")))
        self.assertEqual(labels(sd.PU), set(("p", "ph", "b", "bh", "m")))
        self.assertEqual(labels(sd.SCU), set(("c", "ch", "j", "jh", "ñ", "ś")))
        self.assertEqual(labels(sd.STU), set(("ṭ", "ṭh", "ḍ", "ḍh", "ṇ", "ṣ")))


class RuleTests(unittest.TestCase):
    def test_each_rule_fires_alone_and_leaves_a_trace(self):
        self.assertEqual(sd.final_stop("t", "a").sutras, ("8.2.39",))
        self.assertEqual(sd.final_stop("t", "a").left, "d")
        r = sd.final_stop("t", "c")            # tat + ca -> tac ca
        self.assertEqual((r.left, r.right), ("c", "c"))
        self.assertEqual(r.sutras, ("8.2.39", "8.4.40", "8.4.55"))   # t -> d -> j -> c
        r = sd.final_stop("t", "ṭ")            # tat + ṭa -> taṭ ṭa
        self.assertEqual((r.left, r.right), ("ṭ", "ṭ"))
        self.assertEqual(r.sutras, ("8.2.39", "8.4.41", "8.4.55"))   # t -> d -> q -> w
        r = sd.final_stop("k", "n")            # vak + na -> vaṅ na
        self.assertEqual((r.left, r.right, r.sutras), ("ṅ", "n", ("8.2.39", "8.4.45")))
        r = sd.final_stop("k", "h")            # vak + ha -> vag gha
        self.assertEqual((r.left, r.right, r.sutras), ("g", "gh", ("8.2.39", "8.4.62")))
        r = sd.final_stop("t", "ś")            # tat + śa -> tac cha
        self.assertEqual((r.left, r.right), ("c", "ch"))
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
        self.assertEqual({L[g.nearest(S[x], sd.SCU)] for x in ("s", "th", "d", "dh")} , {"ś", "ch", "j", "jh"})


class VidyutOracleTests(unittest.TestCase):
    """99 rows of vidyut's generated external-sandhi rules for a final k, ṭ, p or t."""

    # Two rows where the implementations disagree because they order rules differently.
    ORDER_DEPENDENT = {("t", "ñ"): ("n", "ñ"), ("t", "ṇ"): ("n", "ṇ")}

    def test_the_fixture_is_the_99_rows(self):
        self.assertEqual(len(oracle("vidyut-sandhi-final-stops.tsv")), 99)

    def test_the_graph_reproduces_97_of_99(self):
        agree, differ = 0, []
        for row in oracle("vidyut-sandhi-final-stops.tsv"):
            first, = oracle_io.names(row["first_iast"])
            second, = oracle_io.names(row["second_iast"])
            (left,), (right,) = oracle_io.parts(row["result_iast"])
            result = (left, right)
            got = sd.final_stop(first, second)
            mine = (got.left, got.right)
            if mine == result:
                agree += 1
            else:
                differ.append((first, second, result, mine))
        self.assertEqual(agree, 97, differ)
        self.assertEqual({(f, s): r for f, s, r, _ in differ}, self.ORDER_DEPENDENT)

    def test_the_two_disagreements_are_a_rule_order_choice_not_a_bug(self):
        # t + ñ: ascending sutra order gives ñ ñ (8.4.40 then 8.4.45); vidyut gives n ñ.
        r = sd.final_stop("t", "ñ")
        self.assertEqual((r.left, r.right, r.sutras), ("ñ", "ñ", ("8.2.39", "8.4.40", "8.4.45")))


class CoqOracleTests(unittest.TestCase):
    """Maps parsed from the Coq formalization `paninian-verified` (definitions as written)."""

    @staticmethod
    def coq(rule):
        return {row["input_iast"]: row["output_iast"] for row in oracle("paninian-verified-consonant-maps.tsv")
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
        self.assertEqual(table["kh"], "gh")
        self.assertEqual(L[g.nearest(S["kh"], sd.JAS)], "g")
        differing = {k for k, v in table.items() if L[g.nearest(S[k], sd.JAS)] != v}
        self.assertEqual(differing, {"kh", "ch", "ṭh", "th", "ph"})   # exactly the five aspirates
        for k in set(table) - differing:
            self.assertEqual(L[g.nearest(S[k], sd.JAS)], table[k])


class ContactTests(unittest.TestCase):
    """8.4.40-44 in both directions; examples tabulated from the Kasika by the shiva agent
    (kAshikAvRRitti.txt lines 83644-83760; second-hand, not re-read here)."""

    def pair(self, left, right, **kw):
        r = sd.contact(left, right, **kw)
        return (r.left, r.right)

    def test_the_dental_changes_before_a_palatal_or_retroflex(self):
        self.assertEqual(self.pair("s", "ś"), oracle_io.names("śś"))        # vrksas sete
        self.assertEqual(self.pair("s", "c"), oracle_io.names("śc"))        # vrksas cinoti
        self.assertEqual(self.pair("t", "ch"), oracle_io.names("cch"))        # agnicic chadayati
        self.assertEqual(self.pair("t", "c"), oracle_io.names("cc"))        # agnicic cinoti
        self.assertEqual(self.pair("s", "ṣ"), oracle_io.names("ṣṣ"))        # vrksas sande
        self.assertEqual(self.pair("d", "ḍ"), oracle_io.names("ḍḍ"))        # agnicid dinah
        self.assertEqual(self.pair("d", "ḍh"), oracle_io.names("ḍḍh"))        # agnicid dhaukate

    def test_and_after_a_palatal_or_retroflex_which_the_left_only_version_missed(self):
        self.assertEqual(self.pair("j", "n"), oracle_io.names("jñ"))        # yajnah  (yaj + nah: n -> ñ)
        self.assertEqual(self.pair("c", "n"), oracle_io.names("cñ"))        # yacna
        self.assertEqual(self.pair("ṣ", "t"), oracle_io.names("ṣṭ"))        # pesta
        self.assertEqual(self.pair("ṣ", "th"), oracle_io.names("ṣṭh"))        # krsistha
        self.assertEqual(self.pair("s", "j"), oracle_io.names("śj"))        # intermediate only: masj -> maśj -> majj (other sutras finish it)

    def test_the_blocks(self):
        r = sd.contact("ś", "n")                           # prasnah, visnah
        self.assertEqual((r.left, r.right, r.blocked), ("ś", "n", ("8.4.44",)))
        self.assertEqual(sd.contact("ś", "t").right, "t")
        r = sd.contact("t", "ṣ")                           # agnicitsande, bhavansande
        self.assertEqual((r.left, r.right, r.blocked), ("t", "ṣ", ("8.4.43",)))
        self.assertEqual(sd.contact("n", "ṣ").left, "n")
        r = sd.contact("ṭ", "s", padanta=True)             # svalit saye
        self.assertEqual((r.left, r.right, r.blocked), ("ṭ", "s", ("8.4.42",)))
        self.assertEqual(sd.contact("ṭ", "t", padanta=True).right, "t")   # madhulit tarati

    def test_inside_a_word_the_same_pair_is_not_blocked_by_8_4_42(self):
        self.assertEqual(self.pair("ṭ", "s"), oracle_io.names("ṭṣ"))

    def test_torli_n_plus_l_gives_the_nasal_l(self):
        # Kasika 8.4.60: bhavaml lunati (a nasal l); t + l gives the oral l
        r = sd.final_stop("n", "l")
        self.assertEqual((r.left, r.sutras), ("l̃", ("8.4.60",)))
        self.assertEqual(sd.final_stop("t", "l").left, "l")

    def test_the_trace_names_the_sutra_and_the_direction(self):
        r = sd.contact("j", "n")
        self.assertEqual([(s.sutra, s.before, s.after) for s in r.trace], [("8.4.40", "n", "ñ")])
        r = sd.contact("t", "c")
        self.assertEqual([(s.sutra, s.before, s.after) for s in r.trace], [("8.4.40", "t", "c")])


class DomainTests(unittest.TestCase):
    """No rule may call `nearest` outside its domain (review by the shiva agent)."""

    def test_no_rule_raises_ambiguous_for_any_pair_of_sounds(self):
        import upc14v2_vowel_sandhi as vs
        labels = list(S) + ["ā", "ī", "ū", "ṝ", "ḹ"]
        for a in labels:
            for b in labels:
                for fn in (sd.final_stop, sd.contact, vs.vowel_sandhi):
                    with self.subTest(rule=fn.__name__, pair=(a, b)):
                        fn(a, b)                                     # must not raise

    def test_a_semivowel_before_a_nasal_becomes_its_own_nasal_form(self):
        # v has two places (teeth, lips): no varga nasal is nearest to it, so 8.4.45 nasalises v itself.
        r = sd.final_stop("v", "n")
        self.assertEqual((r.left, r.sutras), ("ṽ", ("8.4.45",)))
        self.assertEqual(sd.final_stop("y", "m").left, "ỹ")
        self.assertEqual(sd.final_stop("l", "n").left, "l̃")

    def test_r_has_no_nasal_form_so_8_4_45_leaves_it_alone(self):
        # Kasika line 391: y v l have a nasal and a non-nasal form, r has not. The y v l nasal
        # forms are an inference from 391 (the examples of 8.4.45 are all stops).
        r = sd.final_stop("r", "n")
        self.assertEqual((r.left, r.sutras), ("r", ()))

    def test_nearest_is_ambiguous_for_sounds_outside_the_domain_of_yan(self):
        for x in ("k", "kh", "g", "gh", "ṅ", "h", "a"):
            with self.subTest(source=x):
                with self.assertRaises(g.Ambiguous):
                    g.nearest(S[x], sd.YAN)


class NatvaTests(unittest.TestCase):
    def word(self, text):
        return oracle_io.names(text)

    def test_a_word_final_n_is_not_changed_8_4_37(self):
        # Kasika 8.4.37 (line 83569, via the shiva agent): vrksan, plaksan, arin, girin
        for word in ("vṛkṣān", "plakṣān", "arīn", "girīn"):
            with self.subTest(word=word):
                self.assertEqual(sd.natva(self.word(word)), self.word(word))
        # a stem that is not a whole pada still gets natva at its end
        self.assertEqual(sd.natva(self.word("purān"), complete_pada=False), self.word("purāṇ"))

    def test_natva_words(self):
        cases = {
            "rāmena": "rāmeṇa",      # rāmeṇa: r ā m e n a, through ā m e
            "kṛṣṇa": "kṛṣṇa",        # already ṇ after ṣ
            "varna": "varṇa",        # varṇa: n right after r
            "puṇāna": "puṇāna",      # (no n) control
            "purāna": "purāṇa",      # purāṇa
            "brāhmana": "brāhmaṇa",  # brāhmaṇa: through ā h m a
            "arjuna": "arjuna",      # j (a palatal) blocks
            "arthana": "arthana",    # th (a dental) blocks
            "kṛśānu": "kṛśānu",      # ś is neither aṭ, ku nor pu: it blocks
            "nara": "nara",          # n is first: no trigger before it
        }
        for text, want in cases.items():
            with self.subTest(word=text):
                self.assertEqual(sd.natva(self.word(text)), self.word(want))

    def test_the_four_examples_of_the_coq_file(self):
        # natva_ex1..4 of paninian.v: [r a] n -> ṇ ; [a i] n -> n ; [r t a] n -> n ; [ṣ a] n -> ṇ
        for before, want in (("ra", "ṇ"), ("ai", "n"), ("rta", "n"), ("ṣa", "ṇ")):
            with self.subTest(before=before):
                self.assertEqual(sd.natva(oracle_io.names(before) + ("n",), complete_pada=False)[-1], want)   # context test, not a whole pada

    def test_the_through_set_is_at_ku_pu_computed_from_the_graph(self):
        self.assertEqual(len(sd.AT), 13)
        self.assertEqual(labels(sd.NATVA_THROUGH) & set(("ś", "ṣ", "s", "l", "c", "ṭ", "t", "th")), set())

    def test_coq_blocker_list_lets_a_sibilant_through_and_the_graph_query_does_not(self):
        # Coq `is_natva_blocker` lists palatals, retroflexes, dentals and l; the
        # sibilants s' s. s are NOT in it (source-confirmed, Coq not run), so for
        # kṛśānu it would return ṇ. Pāṇini's own set (aṭ, ku, pu) excludes ś, and the
        # graph-computed set keeps n.
        self.assertEqual(sd.natva(oracle_io.names("kṛśānu")), oracle_io.names("kṛśānu"))


if __name__ == "__main__":
    unittest.main()
