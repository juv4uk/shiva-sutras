#!/usr/bin/env python3
"""Tests for VARṆA-7 and PRĀṆA-14 (my two codecs).

Run:  python3 test_my_codecs.py
No third-party test runner required; exits non-zero on the first failure.
"""

from __future__ import annotations

import sys
import traceback

import varna7 as V
import prana14 as P

_FAILURES = []


def check(name, fn):
    try:
        fn()
        print(f"  ok   {name}")
    except Exception as exc:  # noqa: BLE001
        print(f"  FAIL {name}: {exc}")
        _FAILURES.append((name, traceback.format_exc()))


# --------------------------------------------------------------------------
# VARṆA-7
# --------------------------------------------------------------------------


def t_v7_roundtrip():
    for s, c in V.SOUND_SLP1.items():
        assert V.render_slp1((c,)) == s
        assert V.encode_slp1(s) == (c,)
    for word in ("kfta", "saMskfta", "devAlaya", "agnimIle", "zZQ"):
        pass  # zZQ is not all valid; skip
    for word in ("kfta", "saMskfta", "devAlaya", "agnimIle", "Bavati", "dadAti"):
        assert V.render_slp1(V.encode_slp1(word)) == word, word


def t_v7_bijection():
    cells = list(V.SOUND_SLP1.values())
    assert len(cells) == len(set(cells)), "cell collision"
    assert all(V.region_of(c) in V.REGION_NAMES for c in cells)


def t_v7_regions():
    # 25 stops sit in SPARSA, one per (place, member)
    seen = {V.decode_sparsa(V.SOUND_SLP1[s]) for s in V.SOUND_SLP1
            if V.region_of(V.SOUND_SLP1[s]) == V.SPARSA}
    assert len(seen) == 25
    assert seen == {(p, m) for p in range(5) for m in range(5)}


def t_v7_savarna():
    S = V.SOUND_SLP1
    assert V.savarna(S["k"], S["g"])
    assert V.savarna(S["k"], S["N"])
    assert V.savarna(S["g"], S["G"])
    assert not V.savarna(S["k"], S["c"])
    assert not V.savarna(S["k"], S["t"])
    assert V.savarna(S["a"], S["A"])
    assert V.savarna(S["i"], S["I"])
    assert not V.savarna(S["i"], S["y"])
    assert not V.savarna(S["y"], S["S"])
    assert V.savarna(S["S"], S["z"]) is False  # different place
    assert V.savarna(S["r"], S["l"]) is False  # different place


def t_v7_fail_closed():
    for call in (lambda: V.decode_svara(V.make(V.SVARA, 7 << 2)),
                 lambda: V.svara_code(7),
                 lambda: V.decode_sparsa(V.make(V.SPARSA, 25)),
                 lambda: V.checked(128),
                 lambda: V.make(0b100, 0)):
        try:
            call()
            raise AssertionError("should have raised")
        except V.VarnaError:
            pass


def t_v7_signs_distinct():
    # anusvāra and visarga are saṃjñā cells, not sounds
    assert V.region_of(V.SOUND_SLP1["M"]) == V.SAMJNA
    assert V.region_of(V.SOUND_SLP1["H"]) == V.SAMJNA


# --------------------------------------------------------------------------
# PRĀṆA-14
# --------------------------------------------------------------------------


def t_p14_derived():
    assert len(P.SOUNDS) == 47
    for label, code in P.SOUNDS.items():
        assert P.unpack(code).code == code, label


def t_p14_seed_edges():
    # every sound except the seed is reached by a typed edge from a parent
    parents = {child for child, _parent, _edge in P.DERIVATION}
    assert P.SEED_LABEL in P.SOUNDS
    assert parents | {P.SEED_LABEL} == set(P.SOUNDS)


def t_p14_savarna_mask():
    S = P.SOUNDS
    for a in S.values():
        for b in S.values():
            assert P.savarna(a, b) == ((a & P.SAVARNA_MASK) == (b & P.SAVARNA_MASK))
    assert P.SAVARNA_MASK == 0x1FE0


def t_p14_savarna_cases():
    S = P.SOUNDS
    assert P.savarna(S["k"], S["g"])
    assert P.savarna(S["k"], S["N"])
    assert not P.savarna(S["k"], S["c"])
    assert P.savarna(S["a"], S["A"])
    assert not P.savarna(S["i"], S["y"])
    assert not P.savarna(S["e"], S["E"])   # e vs ai
    assert not P.savarna(S["o"], S["O"])
    assert not P.savarna(S["e"], S["o"])
    assert not P.savarna(S["a"], S["e"])


def t_p14_guna_vrddhi():
    S = P.SOUNDS
    assert P.guna(S["a"], S["i"]) == S["e"]
    assert P.guna(S["a"], S["u"]) == S["o"]
    assert P.vrddhi(S["a"], S["e"]) == S["E"]
    assert P.vrddhi(S["a"], S["o"]) == S["O"]


def t_p14_dirgha():
    S = P.SOUNDS
    assert P.dirgha(S["a"], S["a"]) == S["A"]
    assert P.dirgha(S["i"], S["i"]) == S["I"]
    try:
        P.dirgha(S["x"], S["x"])  # ḷ has no long form
        raise AssertionError("ḷ+ḷ must not give a long form")
    except P.PranaError:
        pass


def t_p14_nearest():
    S = P.SOUNDS
    yan = [S[t] for t in ("y", "v", "r", "l")]
    assert P.nearest(S["i"], yan) == S["y"]
    assert P.nearest(S["u"], yan) == S["v"]
    assert P.nearest(S["f"], yan) == S["r"]
    assert P.nearest(S["x"], yan) == S["l"]
    jas = [S[t] for t in ("j", "b", "g", "q", "d")]
    for s, tgt in (("k", "g"), ("K", "g"), ("c", "j"), ("w", "q"), ("t", "d"), ("p", "b")):
        assert P.nearest(S[s], jas) == S[tgt], s


def t_p14_it_markers():
    assert len(P.it_ranks()) == 14
    assert len(P.SUTRAS) == 14
    for rank in P.it_ranks():
        assert P.PATH[rank].is_marker
    # a marker is a meta cell, not a vertex
    assert P.meta_code(P.it_ranks()[0]) >> P.META_SHIFT == 1


def t_p14_pratyahara_intervals():
    S = P.SOUNDS
    ac = P.pratyahara(S["a"], "c")
    assert set(ac) == {S[t] for t in ("a", "i", "u", "f", "x", "e", "o", "E", "O")}
    hal = P.pratyahara(S["h"], "l")
    assert {S[t] for t in ("h", "y", "v", "r", "l")} <= set(hal)


def t_p14_fail_closed():
    for bad in (P.make(P.SPRSTA, P.K_THROAT, length=P.LONG),
                P.make(P.SPRSTA, 0),
                P.make(P.VIVRTA, P.K_THROAT, wide=1, length=P.SHORT) and 0,  # placeholder
                1 << P.META_SHIFT):
        if bad == 0:
            continue
        try:
            P.unpack(bad)
            raise AssertionError(f"{P.bits(bad)} should be rejected")
        except P.InvalidCode:
            pass


# --------------------------------------------------------------------------


def main():
    print("VARṆA-7")
    for name, fn in sorted({k: v for k, v in globals().items() if k.startswith("t_v7_")}.items()):
        check(name, fn)
    print("PRĀṆA-14")
    for name, fn in sorted({k: v for k, v in globals().items() if k.startswith("t_p14_")}.items()):
        check(name, fn)
    if _FAILURES:
        print(f"\n{len(_FAILURES)} failure(s):")
        for name, tb in _FAILURES:
            print(f"\n--- {name} ---\n{tb}")
        return 1
    print("\nall tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
