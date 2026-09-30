#!/usr/bin/env python3
"""
Consonant sandhi as graph queries (shiva-sutras#44, experiment)
===============================================================

A step from the Siva-sutras toward the Astadhyayi. Every sound class a rule
needs is *computed from the graph* (`upc14v2`), never listed:

    jhal jas jhas khar car yar nam jhay at      intervals of the sutra path
    ku cu wu tu pu                              savarna classes of a varga
    scu = cu + s'      stu = wu + s.            unions of the above

and every substitution is the same query: the NEAREST vertex of a target set
(1.1.50, sthane'ntaratamah). A rule is (sutra number, guard, target set). The
result carries the trace of the sutras that fired, so a derivation is visible.

Order. Rules are applied once each, in ascending sutra number
(8.2.39, 8.4.40, 8.4.41, 8.4.60, 8.4.45, 8.4.55/53, 8.4.62, 8.4.63). That is one
choice: the tradition orders conflicting rules by vipratisedha (1.4.2), and
implementations differ (see `test_upc14v2_sandhi.py`).

Scope: pada-final stops meeting the next sound (external sandhi), and natva
(8.4.2) inside a word. Anusvara, visarga, the sibilant insertions of `n` and all
vowel sandhi are outside this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, List, Optional, Sequence, Tuple

import upc14v2 as g

S = g.SOUNDS
L = g.LABELS_BY_CODE

# A long vowel is not a 43rd sound: it is the short vertex one step along the length path.
_LONG = {"A": "a", "I": "i", "U": "u", "F": "f", "X": "x"}


def code_of(label: str) -> int:
    if label in S:
        return S[label]
    if label in _LONG:
        return g.e_long(S[_LONG[label]])
    raise g.GraphError(f"{label!r} is not a sound of this graph")


def base(code: int) -> int:
    """The short, oral vertex a vowel form stands for (length and nose are ignored by a class)."""
    v = g.unpack(code)
    if v.aperture >= g.VOWEL and (v.length or v.nasal):
        short = g.Vertex(v.place, 0, v.aperture, 0 if v.aperture == g.VOWEL else v.length, v.voice, v.asp).code
        if short in L:
            return short
        long_by_nature = g.Vertex(v.place, 0, v.aperture, v.length, v.voice, v.asp).code
        if long_by_nature in L:
            return long_by_nature
    return code


def label_of(code: int) -> str:
    if code in L:
        return L[code]
    for long_label, short in _LONG.items():
        if code == g.e_long(S[short]):
            return long_label
    v = g.unpack(code)
    if v.nasal:                                         # the nasal form of a labelled vertex: `~`, as in SLP1
        plain = g.Vertex(v.place, 0, v.aperture, v.length, v.voice, v.asp).code
        if plain in L:
            return L[plain] + "~"
    raise g.GraphError(f"{g.bits(code)} has no debug label")


def _p(start: str, marker: str, nth: int = 1) -> FrozenSet[int]:
    return frozenset(g.pratyahara(S[start], marker, nth))


def _varga(letter: str) -> FrozenSet[int]:
    """A varga incl. its nasal: the stops savarna with `letter` (the `ku~` `cu~` ... classes)."""
    return frozenset(c for c in S.values()
                     if g.unpack(c).aperture == g.STOP and g.savarna(S[letter], c))


# Pratyaharas: intervals of the sutra path.
JHAL = _p("J", "l")
JAS = _p("j", "S")
JHAS = _p("J", "S")       # jhas in SLP1 `JaS`
KHAR = _p("K", "r")
CAR = _p("c", "r")
YAR = _p("y", "r")
YAN = _p("y", "R")
NAM = _p("Y", "m")
JHAY = _p("J", "y")
AT = _p("a", "w")
# Savarna classes.
KU, CU, WU, TU, PU = (_varga(x) for x in "kcwtp")
SCU = CU | {S["S"]}
STU = WU | {S["z"]}


@dataclass(frozen=True)
class Step:
    sutra: str
    before: str
    after: str


@dataclass(frozen=True)
class Result:
    left: str
    right: str
    trace: Tuple[Step, ...]
    blocked: Tuple[str, ...] = ()   # sutras that stopped a substitution which would otherwise have fired

    @property
    def sutras(self) -> Tuple[str, ...]:
        return tuple(step.sutra for step in self.trace)


def _fourth_of(left: int) -> Optional[int]:
    """The voiced aspirated stop of the varga `left` belongs to (8.4.62)."""
    for c in S.values():
        v = g.unpack(c)
        if v.aperture == g.STOP and v.voice and v.asp and g.savarna(left, c):
            return c
    return None


def final_stop(left: str, right: str, after: Optional[str] = "a") -> Result:
    """A pada-final stop `left` meets the first sound `right` of the next word.

    `after` is the sound that follows `right` (8.4.63 needs it); default: a vowel.
    Letters are SLP1 debug labels; the work is done on vertices.
    """
    l, r = code_of(left), code_of(right)
    r_out = r
    trace: List[Step] = []

    def fire(sutra: str, old: int, new: int) -> int:
        if new != old:
            trace.append(Step(sutra, label_of(old), label_of(new)))
        return new

    if l in JHAL:                                                   # 8.2.39 jhalam jaso'nte
        l = fire("8.2.39", l, g.nearest(l, JAS))
    if (l in TU or l == S["s"]) and r in SCU:                       # 8.4.40 stoh scuna scuh
        l = fire("8.4.40", l, g.nearest(l, SCU))
    elif (l in TU or l == S["s"]) and r in STU:                     # 8.4.41 stuna stuh
        l = fire("8.4.41", l, g.nearest(l, STU))
    if l in TU and right == "l":                                    # 8.4.60 tor li
        l = fire("8.4.60", l, S["l"])
    if l in YAR and r in NAM:                                       # 8.4.45 yaro'nunasike'nunasiko va
        if l == S["r"]:                                             # Kasika 391: r has no nasal form
            pass
        elif l in YAN:                                              # y v l: their own nasal form (an
            v = g.unpack(l)                                         # inference from 391), not a varga nasal
            l = fire("8.4.45", l, g.Vertex(v.place, 1, v.aperture, v.length, v.voice, v.asp).code)
        else:
            l = fire("8.4.45", l, g.nearest(l, NAM))
    elif l in JHAL and r in KHAR:                                   # 8.4.55 khari ca
        l = fire("8.4.55", l, g.nearest(l, CAR))
    if right == "h" and l in JHAY:                                  # 8.4.62 jhayo ho'nyatarasyam
        fourth = _fourth_of(l)
        if fourth is not None:
            r_out = fire("8.4.62", r, fourth)
    if right == "S" and code_of(left) in JHAY and after and base(code_of(after)) in AT:   # 8.4.63 sas cho'ti
        r_out = fire("8.4.63", r, S["C"])
    return Result(label_of(l), label_of(r_out), tuple(trace))


# ---------------------------------------------------------------------------
# 8.4.40-44: scutva and stutva in contact, in BOTH directions, with their blocks
# ---------------------------------------------------------------------------


def contact(left: str, right: str, *, padanta: bool = False) -> Result:
    """Place assimilation of two adjacent consonants (`s`/t-varga meeting a palatal or retroflex).

    The Kasika says 8.4.40 and 8.4.41 act whether the s/t-varga comes BEFORE or AFTER the
    palatal/retroflex (it argues so from 8.4.44 itself, kAshikAvRRitti.txt lines 83644-83721,
    quoted by the shiva agent). The blocks come first, as they stop the substitution itself:

        8.4.42  a word-final ṭ-varga does not make a following s/t-varga retroflex (`padanta`)
        8.4.43  a t-varga before ṣ does not become retroflex
        8.4.44  after ś a t-varga does not become palatal

    Not implemented: the exceptions of 8.4.42 (nam, navati, nagari), which need morphology,
    and voicing (8.4.53/55), which `final_stop` applies.
    """
    l, r = code_of(left), code_of(right)
    dental_l = l in TU or l == S["s"]
    dental_r = r in TU or r == S["s"]
    trace: List[Step] = []
    blocked: List[str] = []

    def fire(sutra: str, old: int, new: int) -> int:
        if new != old:
            trace.append(Step(sutra, label_of(old), label_of(new)))
        return new

    left_palatal = dental_l and r in SCU
    right_palatal = dental_r and l in SCU
    left_retro = dental_l and r in STU
    right_retro = dental_r and l in STU
    if right_palatal and l == S["S"] and r in TU:                       # 8.4.44 sat
        right_palatal = False
        blocked.append("8.4.44")
    if left_retro and l in TU and r == S["z"]:                          # 8.4.43 toh si
        left_retro = False
        blocked.append("8.4.43")
    if right_retro and padanta and l in WU and (r in TU or r == S["s"]):    # 8.4.42
        right_retro = False
        blocked.append("8.4.42")
    if left_palatal:
        l = fire("8.4.40", l, g.nearest(l, SCU))
    if right_palatal:
        r = fire("8.4.40", r, g.nearest(r, SCU))
    if left_retro:
        l = fire("8.4.41", l, g.nearest(l, STU))
    if right_retro:
        r = fire("8.4.41", r, g.nearest(r, STU))
    return Result(label_of(l), label_of(r), tuple(trace), tuple(blocked))


# ---------------------------------------------------------------------------
# 8.4.2 natva: n becomes ṇ after r, ṣ (or ṛ) within a word, through aṭ, ku, pu
# ---------------------------------------------------------------------------

NATVA_TRIGGERS = frozenset({S["r"], S["z"], S["f"]})
# What may stand between trigger and n (aṭ-kupvāṅnumvyavāye'pi). `āṅ` and `num` are not modelled.
NATVA_THROUGH = AT | KU | PU


def natva(word: Sequence[str]) -> Tuple[str, ...]:
    """Apply 8.4.2 to a word given as SLP1 debug labels; return the labels."""
    out = list(word)
    for i, label in enumerate(word):
        if code_of(label) != S["n"]:
            continue
        j = i - 1
        while j >= 0 and base(code_of(word[j])) in NATVA_THROUGH and base(code_of(word[j])) not in NATVA_TRIGGERS:
            j -= 1
        if j >= 0 and base(code_of(word[j])) in NATVA_TRIGGERS:
            out[i] = "R"
    return tuple(out)


__all__ = [
    "AT", "CAR", "CU", "JAS", "JHAL", "JHAS", "JHAY", "KHAR", "KU", "NAM", "NATVA_THROUGH",
    "PU", "Result", "SCU", "STU", "Step", "TU", "WU", "YAN", "YAR", "base", "code_of", "contact", "final_stop", "label_of", "natva",
]
