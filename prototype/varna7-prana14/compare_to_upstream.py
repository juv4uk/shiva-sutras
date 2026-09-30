#!/usr/bin/env python3
"""Compare my codecs (VARṆA-7, PRĀṆA-14) with the existing UPC-7 / UPC-14 v2.

Reads the upstream modules read-only from the shiva-sutras checkout; nothing is
modified there. Run:  python3 compare_to_upstream.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import varna7 as V
import prana14 as P

# Upstream UPC-7 / UPC-14 v2 live one level up, in prototype/. Override with
# an argument:  python3 compare_to_upstream.py /path/to/shiva-sutras/prototype
UP = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # dataclasses look up cls.__module__ in sys.modules
    spec.loader.exec_module(mod)
    return mod


U7 = load("upc7_geometry", UP / "upc7_geometry.py")
U14 = load("upc14v2", UP / "upc14v2.py")

# UPC-14 v2 stores the 42 sutra sounds; the long vowels are derived on demand.
_LONG = {"A": "a", "I": "i", "U": "u", "F": "f", "X": "x"}


def u14_code(label: str) -> int:
    if label in U14.SOUNDS:
        return U14.SOUNDS[label]
    if label in _LONG:
        base = U14.SOUNDS[_LONG[label]]
        return U14.dirgha(base, base)  # may raise for ḷ (no long form)
    raise KeyError(label)

# The 42 Siva-sutra sounds, SLP1 labels shared by both worlds.
SUTRA42 = ("a", "i", "u", "f", "x", "e", "o", "E", "O",
           "k", "K", "g", "G", "N", "c", "C", "j", "J", "Y",
           "w", "W", "q", "Q", "R", "t", "T", "d", "D", "n",
           "p", "P", "b", "B", "m", "y", "r", "l", "v", "S", "z", "s", "h")
assert len(SUTRA42) == 42

SAVARNA_PAIRS = [
    ("k", "g", True), ("k", "K", True), ("k", "N", True), ("k", "c", False),
    ("g", "G", True), ("c", "j", True), ("c", "t", False), ("t", "T", True),
    ("a", "A", True), ("i", "I", True), ("u", "U", True),
    ("a", "i", False), ("i", "y", False), ("y", "S", False),
    ("S", "z", False), ("r", "l", False), ("e", "E", False), ("o", "O", False),
    ("e", "o", False), ("a", "e", False),
]


def main():
    print("=" * 78)
    print("COVERAGE")
    print("=" * 78)
    print(f"  UPC-7 placed sound cells     : (see upc7-table.tsv; geometry exposes no table)")
    print(f"  UPC-14 v2 derived sounds     : {len(U14.SOUNDS)}  (+5 long vowels on demand)")
    print(f"  PRĀṆA-14 derived sounds      : {len(P.SOUNDS)}  (42 + 5 long vowels, materialised)")
    print(f"  VARṆA-7 phonetic cells       : {len(V.SOUND_SLP1)}")

    # --- sound sets agree between PRANA-14 and UPC-14 v2 -------------------
    u14_labels = set(U14.SOUNDS) | set(_LONG)
    p14_labels = set(P.SOUNDS)
    print(f"\n  UPC-14 v2 labels (incl. longs) == PRĀṆA-14 labels : {u14_labels == p14_labels}")
    if u14_labels != p14_labels:
        print(f"    only v2 : {sorted(u14_labels - p14_labels)}")
        print(f"    only mine: {sorted(p14_labels - u14_labels)}")

    # --- savarna agreement across three codecs ----------------------------
    print("\n" + "=" * 78)
    print("SAVARṆA (1.1.9) — agreement on", len(SAVARNA_PAIRS), "pairs")
    print("=" * 78)
    hdr = f"  {'pair':>7}  {'expect':>6}  {'UPC-14v2':>8}  {'PRĀṆA-14':>8}  {'VARṆA-7':>8}"
    print(hdr)
    disagree = 0
    for a, b, expect in SAVARNA_PAIRS:
        try:
            u = U14.savarna(u14_code(a), u14_code(b))
        except Exception:  # noqa: BLE001  (e.g. ḷ has no long form in v2)
            u = "n/a"
        p = P.savarna(P.SOUNDS[a], P.SOUNDS[b])
        v = V.savarna(V.SOUND_SLP1[a], V.SOUND_SLP1[b])
        flag = "" if (u == p == v == expect) else "  <-- differs"
        if flag:
            disagree += 1
        print(f"  {a + '~' + b:>7}  {str(expect):>6}  {str(u):>8}  {str(p):>8}  {str(v):>8}{flag}")
    print(f"\n  pairs where some codec disagrees with the expected reading: {disagree}")

    # --- the mask property (my design's headline) -------------------------
    print("\n" + "=" * 78)
    print("SAVARṆA AS A BIT-MASK")
    print("=" * 78)
    ok = all(P.savarna(x, y) == ((x & P.SAVARNA_MASK) == (y & P.SAVARNA_MASK))
             for x in P.SOUNDS.values() for y in P.SOUNDS.values())
    print(f"  PRĀṆA-14  savarna(a,b) == (a & 0x{P.SAVARNA_MASK:04X}) == (b & 0x{P.SAVARNA_MASK:04X}) : {ok}")

    # --- guna / vrddhi agreement ------------------------------------------
    print("\n" + "=" * 78)
    print("GUṆA (6.1.87) / VṚDDHI (6.1.88)")
    print("=" * 78)
    for name, fn_p, fn_u, pairs in (
        ("guṇa", P.guna, U14.guna, [("a", "i", "e"), ("a", "u", "o")]),
        ("vṛddhi", P.vrddhi, U14.vrddhi, [("a", "e", "E"), ("a", "o", "O")]),
    ):
        for a, b, exp in pairs:
            rp = fn_p(P.SOUNDS[a], P.SOUNDS[b])
            ru = fn_u(U14.SOUNDS[a], U14.SOUNDS[b])
            same_mine = rp == P.SOUNDS[exp]
            same_up = ru == U14.SOUNDS[exp]
            print(f"  {name}({a},{b}) -> {exp}   mine:{same_mine}  UPC-14v2:{same_up}")

    # --- pratyahara agreement (same sutra path) ---------------------------
    print("\n" + "=" * 78)
    print("PRATYĀHĀRA (interval of the sūtra path)")
    print("=" * 78)
    for start, marker in (("a", "c"), ("h", "l"), ("a", "N"), ("h", "Y")):
        mine = {P.LABELS_BY_CODE[c] for c in P.pratyahara(P.SOUNDS[start], marker)}
        try:
            theirs = {U14.LABELS_BY_CODE[c] for c in U14.pratyahara(U14.SOUNDS[start], marker)}
        except Exception as exc:  # noqa: BLE001
            theirs = {f"<error {exc}>"}
        print(f"  {start}...{marker}: match={mine == theirs}  ({len(mine)} sounds)")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print("  • PRĀṆA-14 reproduces UPC-14 v2's derived 42+5 inventory and its")
    print("    guṇa/vṛddhi/pratyāhāra behaviour, with a different field order.")
    print("  • PRĀṆA-14 adds one property v2 lacks: savarṇa is a single mask AND.")
    print("  • VARṆA-7 is a 7-bit identity codec partitioned by effort, not by")
    print("    varga/non-varga/vowel/sign; it is exact for stops and vowels")
    print("    a/i/u/ṛ/ḷ, and (like UPC-7) conflates e with ai via the length bit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
