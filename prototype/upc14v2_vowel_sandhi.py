#!/usr/bin/env python3
"""
Vowel sandhi as graph queries (shiva-sutras#44, experiment)
===========================================================

The next step after consonant sandhi (`upc14v2_sandhi`). Same method: every
class is computed from the graph (pratyahara = interval of the sutra path,
savarna = equal place and aperture) and every substitution is a query on it.

    6.1.101 akah savarne dirghah      ak + savarna ac        -> the long vowel
    6.1.88  vrddhir eci               a + ec                 -> place join, aperture lifted
    6.1.87  ad gunah                  a + ik                 -> place join (ṛ, ḷ: + r, l: 1.1.51)
    6.1.77  iko yan aci               ik + ac                -> the nearest semivowel (yan)
    6.1.78  eco 'yavayavah            ec + ac                -> decompose the join, yan the second
    6.1.109 enah padantad ati         e/o (word-final) + a   -> the e/o stays, a is elided (apavada of 6.1.78)
    6.1.97  ato gune                  a (inside a word) + a/e/o -> the following sound (apavada of 6.1.101)

Rules are tried in this order (the savarna case first: it is what stops 6.1.87
from also firing on a + a). A result is the SEQUENCE of sounds that replaces
the pair, with the trace of sutras that fired. Length and nose of a vowel are
coordinates, so the classes ignore them (`base`).

Under the adhikara 6.1.84 (`ekah purvaparayoh`, valid up to and including 6.1.111 per the
Kasika) the pair becomes ONE sound (ekadesa): 6.1.87, 88, 97, 101, 109. 6.1.77 and 6.1.78
stand BEFORE 6.1.84 and replace a single sound, so the result carries `ekadesa`.
(Source: the Kasika text as tabulated by the panini agent; not re-read here.)

Not implemented, on purpose: 6.1.94 (eni pararupam), the plutapurva exception of 6.1.77,
the optional elision of y/v (8.3.19), the avagraha sign after e/o, and every condition
that needs morphology (a dhatu, an upasarga, a suffix). `padanta` says whether the pair
is at a word boundary (default) or inside a word.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Optional, Tuple

import upc14v2 as g
import upc14v2_sandhi as sd

S = g.SOUNDS
label_of, code_of, base = sd.label_of, sd.code_of, sd.base


def _p(start: str, marker: str) -> FrozenSet[int]:
    return frozenset(g.pratyahara(S[start], marker))


AC = _p("a", "c")
AK = _p("a", "k")
IK = _p("i", "k")
EC = _p("e", "c")
YAN = _p("y", "R")


ADHIKARA_EKADESA = (84, 111)   # 6.1.84 ekah purvaparayoh .. 6.1.111 inclusive (Kasika)


def under_ekadesa(sutra: str) -> bool:
    """Does the sutra `6.1.N` stand under the adhikara 6.1.84 (pair -> one sound)?"""
    parts = sutra.split(".")
    if parts[:2] != ["6", "1"] or len(parts) != 3:
        return False
    return ADHIKARA_EKADESA[0] < int(parts[2]) <= ADHIKARA_EKADESA[1]


@dataclass(frozen=True)
class Result:
    sounds: Tuple[str, ...]
    trace: Tuple[str, ...]

    @property
    def text(self) -> str:
        return "".join(self.sounds)

    @property
    def ekadesa(self) -> bool:
        """True when the first sutra that fired replaces the PAIR by one sound."""
        return bool(self.trace) and under_ekadesa(self.trace[0])


_ATOM_VOWEL = {g.K: "a", g.T: "i", g.O: "u", g.M: "f", g.D: "x"}


def decompose(code: int) -> Tuple[int, int]:
    """Split a vowel that is the JOIN of two places into its two simple vowels.

    e = a + i, o = a + u; ai = long a + i, au = long a + u (the aperture lift of
    vrddhi shows as the long first part). Ordered along the place spine.
    """
    v = g.unpack(code)
    atoms = [a for a in g.PLACE_SPINE if v.place & a]
    if len(atoms) != 2 or v.aperture < g.VOWEL:
        raise g.GraphError(f"{g.bits(code)} is not a join of two vowels")
    first, second = (S[_ATOM_VOWEL[a]] for a in atoms)
    if v.aperture == g.WIDE_VOWEL:
        first = g.e_long(first)
    return first, second


def vowel_sandhi(left: str, right: str, *, padanta: bool = True) -> Result:
    """Two vowels meet; return the sounds that replace them. `padanta`: at a word boundary."""
    l, r = code_of(left), code_of(right)
    bl, br = base(l), base(r)
    if not padanta and l == S["a"] and r in (S["a"], S["e"], S["o"]):   # 6.1.97 ato gune (a is tapara: short)
        return Result((label_of(r),), ("6.1.97",))
    if padanta and bl in (S["e"], S["o"]) and r == S["a"]:           # 6.1.109 (apavada of 6.1.78; ati is tapara: short a)
        return Result((label_of(l),), ("6.1.109",))
    if bl in AK and br in AC and g.savarna(l, r):                    # 6.1.101
        merged = g.dirgha(bl, br)
        return Result((label_of(merged),), ("6.1.101",))
    if bl == S["a"] and br in EC:                                    # 6.1.88
        return Result((label_of(g.vrddhi(bl, br)),), ("6.1.88",))
    if bl == S["a"] and br in IK:                                    # 6.1.87
        if br in (S["f"], S["x"]):                                   # 1.1.51 uran raparah
            return Result((label_of(bl), label_of(g.nearest(br, YAN))), ("6.1.87", "1.1.51"))
        return Result((label_of(g.guna(bl, br)),), ("6.1.87",))
    if bl in IK and br in AC:                                        # 6.1.77
        return Result((label_of(g.nearest(bl, YAN)), label_of(r)), ("6.1.77",))
    if bl in EC and br in AC:                                        # 6.1.78
        first, second = decompose(bl)
        return Result((label_of(first), label_of(g.nearest(second, YAN)), label_of(r)), ("6.1.78",))
    return Result((label_of(l), label_of(r)), ())


__all__ = ["AC", "AK", "ADHIKARA_EKADESA", "EC", "IK", "Result", "YAN", "decompose", "under_ekadesa", "vowel_sandhi"]
