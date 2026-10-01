#!/usr/bin/env python3
"""A survey of the 7-bit prototypes of the project (research, hypothesis; read-only: changes none of them).

For each prototype it builds {sound (IAST name): 7-bit cell} for the 42 sounds and measures the same
things, so the prototypes can be compared on evidence instead of descriptions:

  H  hand-placed UPC-7 table (upc7-table.tsv, geometry v2)           = what SENS pins as Text7
  D  UPC-7 derived from the UPC-14 graph (upc7_derive.py)
  V  VARNA-7 (varna7-prana14/varna7.py)
  A  AKSHARA-7 (akshara7.py)
  T  TANTU-7 (graph7.py)
  L  legacy UPC-7 (upc7.py): the low half of the flat UPC-8 table (its codes are the sutra order)

Measured: coverage and distinctness of the 42 cells; pairwise agreement; whether the 43 pratyaharas are
contiguous in code order; how well a structure-only savarna rule (place + effort read from the bits)
agrees with the graph's 1.1.9; free cells.
"""

from __future__ import annotations

import csv
import itertools
import json
import os
import sys
from typing import Callable, Dict, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "varna7-prana14"))

import oracle_io  # noqa: E402
import upc14v2 as g  # noqa: E402
import upc14v2_sandhi as sd  # noqa: E402

S = g.SOUNDS
SOUNDS = tuple(S)

# SLP1 -> IAST, needed ONLY to read prototypes that still spell their cells in SLP1 (varna7, upc8)
_SLP1 = {"A": "ā", "I": "ī", "U": "ū", "f": "ṛ", "F": "ṝ", "x": "ḷ", "X": "ḹ", "E": "ai", "O": "au", "K": "kh",
         "G": "gh", "N": "ṅ", "C": "ch", "J": "jh", "Y": "ñ", "w": "ṭ", "W": "ṭh", "q": "ḍ", "Q": "ḍh", "R": "ṇ",
         "T": "th", "D": "dh", "P": "ph", "B": "bh", "S": "ś", "z": "ṣ"}


def iast_of_slp1(key: str) -> str:
    return _SLP1.get(key, key)


def cells_hand() -> Dict[str, int]:
    out = {}
    with open(os.path.join(HERE, "upc7-table.tsv"), encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["status"] == "assigned" and row["sa-iast"]:
                out[row["sa-iast"]] = int(row["bits"], 2)
    return out


def cells_derived() -> Dict[str, int]:
    import upc7_derive as d
    return {n: d.derive(sd.code_of(n)) for n in list(SOUNDS) + ["ā", "ī", "ū", "ṝ"]}


def cells_varna() -> Dict[str, int]:
    import varna7
    return {iast_of_slp1(k): c for k, c in varna7.SOUND_SLP1.items() if iast_of_slp1(k) in SOUNDS
            or iast_of_slp1(k) in ("ā", "ī", "ū", "ṝ", "ḹ")}


def cells_akshara() -> Dict[str, int]:
    import akshara7
    return dict(akshara7.SOUND_CODE)


def cells_tantu() -> Dict[str, int]:
    import graph7
    return dict(graph7.NAME_TO_NODE)


def cells_legacy() -> Dict[str, int]:
    import upc8
    return {iast_of_slp1(k): c for k, c in upc8.CODE_OF_SOUND.items()}


PROTOTYPES = (("H", "hand-placed UPC-7 table", cells_hand), ("D", "UPC-7 derived from the UPC-14 graph", cells_derived),
              ("V", "VARNA-7", cells_varna), ("A", "AKSHARA-7", cells_akshara), ("T", "TANTU-7", cells_tantu),
              ("L", "legacy UPC-7 (sutra order)", cells_legacy))

PRATYAHARA_SETS: List[Tuple[str, frozenset]] = []


def pratyahara_sets() -> List[Tuple[str, frozenset]]:
    if not PRATYAHARA_SETS:
        for row in oracle_io.rows("ashtadhyayi-com-pratyahara.tsv"):
            PRATYAHARA_SETS.append((row["name_iast"], frozenset(oracle_io.names(row["sounds_iast"]))))
    return PRATYAHARA_SETS


def contiguous(cells: Dict[str, int], names: frozenset) -> Optional[bool]:
    """Are the cells of `names` consecutive integers? None when a sound has no cell."""
    if not all(n in cells for n in names):
        return None
    values = sorted(cells[n] for n in names)
    return values[-1] - values[0] == len(values) - 1


def structural_savarna(key: str, cells: Dict[str, int]) -> Optional[Callable[[int, int], bool]]:
    """A rule that reads place + effort from the BITS of a cell, where the prototype has such structure."""
    if key in ("H", "D", "V"):
        def rule(a: int, b: int) -> bool:
            ca, cb = a >> 5, b >> 5
            if ca != cb:
                return False
            pa, pb = a & 31, b & 31
            if ca == 0:
                return pa // 5 == pb // 5                       # varga: same place row
            if ca == 1:
                return (pa >> 2) == (pb >> 2) and ((pa & 3) >> 1) == ((pb & 3) >> 1) if False else \
                    (pa >> 2) == (pb >> 2) and _kind_effort(pa & 3) == _kind_effort(pb & 3)
            if ca == 2:
                return (pa >> 2) == (pb >> 2)                   # vowel row (length / nose ignored)
            return False
        return rule
    return None


def _kind_effort(kind: int) -> str:
    return "ushma" if kind in (0, 1) else "ishat"


def measure() -> Dict[str, dict]:
    report: Dict[str, dict] = {}
    for key, label, build in PROTOTYPES:
        try:
            cells = build()
        except Exception as exc:                                  # a prototype that cannot even be read
            report[key] = {"name": label, "error": repr(exc)}
            continue
        sound_cells = {n: cells[n] for n in SOUNDS if n in cells}
        values = list(sound_cells.values())
        rule = structural_savarna(key, cells)
        mismatch = None
        if rule is not None:
            mismatch = sum(1 for a, b in itertools.product(sound_cells, repeat=2)
                           if rule(sound_cells[a], sound_cells[b]) != g.savarna(S[a], S[b]))
        pr = [contiguous(cells, names) for _, names in pratyahara_sets()]
        report[key] = {
            "name": label,
            "of_42_sounds": len(sound_cells),
            "distinct": len(set(values)),
            "extra_cells_named": sorted(n for n in cells if n not in SOUNDS),
            "max_cell": max(values),
            "pratyaharas_contiguous": f"{sum(1 for x in pr if x)}/{sum(1 for x in pr if x is not None)}",
            "savarna_from_bits_mismatches_of_1764": mismatch,
        }
    # pairwise agreement on the 42 sounds
    keys = [k for k, _, _ in PROTOTYPES if "error" not in report[k]]
    built = {k: next(b for kk, _, b in PROTOTYPES if kk == k)() for k in keys}
    agree = {}
    for a, b in itertools.combinations(keys, 2):
        same = sum(1 for n in SOUNDS if n in built[a] and n in built[b] and built[a][n] == built[b][n])
        agree[f"{a}-{b}"] = same
    report["pairwise_equal_cells_of_42"] = agree
    return report


if __name__ == "__main__":
    print(json.dumps(measure(), ensure_ascii=False, indent=2))
