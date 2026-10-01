#!/usr/bin/env python3
"""An independent oracle for vowel sandhi (6.1.77, 6.1.78, 6.1.87, 6.1.88, 6.1.97, 6.1.101, 6.1.109).

Written from the sutras and the Kasika as plain IAST string rules; it does not import or read `upc14v2_vowel_sandhi`.
Every ordered pair of the 13 vowels (a ā i ī u ū ṛ ṝ ḷ e ai o au), both word-final (padanta) and word-internal: 338 pairs.
Written by the shiva agent, 2026-10-02. Hypothesis-level check: the order of the rules is the usual apavada order
(97 / 101 before 88 / 87 before 77; 109 before 78), which the module's docstring also states.
"""

import unittest

import upc14v2_vowel_sandhi as v

VOWELS = ["a", "ā", "i", "ī", "u", "ū", "ṛ", "ṝ", "ḷ", "e", "ai", "o", "au"]
LONG = {"a": "ā", "i": "ī", "u": "ū", "ṛ": "ṝ"}
CLASS = {"a": "a", "ā": "a", "i": "i", "ī": "i", "u": "u", "ū": "u", "ṛ": "ṛ", "ṝ": "ṛ", "ḷ": "ḷ"}   # 1.1.9, without the vartika
AK = set(CLASS)
IK = {"i", "ī", "u", "ū", "ṛ", "ṝ", "ḷ"}
EC = {"e", "ai", "o", "au"}
YAN = {"i": "y", "ī": "y", "u": "v", "ū": "v", "ṛ": "r", "ṝ": "r", "ḷ": "l"}
GUNA = {"i": ["e"], "ī": ["e"], "u": ["o"], "ū": ["o"], "ṛ": ["a", "r"], "ṝ": ["a", "r"], "ḷ": ["a", "l"]}
AYAV = {"e": ["a", "y"], "o": ["a", "v"], "ai": ["ā", "y"], "au": ["ā", "v"]}


def rule_of(left, right, padanta):
    """(rule, sounds) of the oracle."""
    if left == "a" and right in ("a", "e", "o") and not padanta:
        return "6.1.97", [right]
    if left in AK and right in AK and CLASS[left] == CLASS[right]:
        return "6.1.101", [LONG.get(CLASS[left], "ṝ")]
    if left in ("a", "ā") and right in EC:
        return "6.1.88", ["ai" if right in ("e", "ai") else "au"]
    if left in ("a", "ā") and right in IK:
        return "6.1.87", list(GUNA[right])
    if left in IK:
        return "6.1.77", [YAN[left], right]
    if padanta and left in ("e", "o") and right == "a":
        return "6.1.109", [left]
    return "6.1.78", AYAV[left] + [right]


# The one class where the module and this oracle differ (2 of 338 pairs: ḷ + ḷ, either position). The Kasika has no
# rule for it without the vartika (the dirgha of ḷ does not exist, txt 389); with `vartika=True` the module gives ṝ with
# the option ḷ, which is what «लृति लृ वा» and «दीर्घपक्षे ... ऋकारः क्रियते» say.
KNOWN_DIFFERENCE = {("ḷ", "ḷ")}


class VowelOracleTests(unittest.TestCase):
    def test_every_pair_agrees_except_the_known_difference(self):
        diffs, per_rule = [], {}
        for padanta in (True, False):
            for left in VOWELS:
                for right in VOWELS:
                    rule, expected = rule_of(left, right, padanta)
                    result = v.vowel_sandhi(left, right, padanta=padanta)
                    per_rule.setdefault(rule, [0, 0])[0] += 1
                    if list(result.sounds) == expected and result.trace[0] == rule:
                        per_rule[rule][1] += 1
                    else:
                        diffs.append((padanta, left, right, rule, expected, list(result.sounds), result.trace))
        self.assertEqual({(d[1], d[2]) for d in diffs}, KNOWN_DIFFERENCE, diffs)
        self.assertEqual(len(diffs), 2)
        self.assertEqual(sum(n for n, _ in per_rule.values()), 338)

    def test_the_known_difference_is_what_it_is(self):
        self.assertEqual(list(v.vowel_sandhi("ḷ", "ḷ").sounds), ["l", "ḷ"])
        with_vartika = v.vowel_sandhi("ḷ", "ḷ", vartika=True)
        self.assertEqual(list(with_vartika.sounds), ["ṝ"])
        self.assertIn(("ḷ",), with_vartika.options)


if __name__ == "__main__":
    unittest.main()
