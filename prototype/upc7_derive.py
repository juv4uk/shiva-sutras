#!/usr/bin/env python3
"""saṅkṣepa7 (संक्षेप, "abridgment"): UPC-7 as a derived projection of the UPC-14 graph (experiment, hypothesis).

New paradigm: a UPC-7 cell is not placed by hand in a table, it is COMPUTED from the UPC-14 vertex
(`upc14v2`): the 2-bit class from the aperture, the payload from the place and the edges. This
module states those rules and compares the result with the placed cells of `upc7-table.tsv`
(`upc7_geometry`, the hand design). Where they differ, the difference is reported, not hidden.

    class     aperture: stop 00, semivowel/sibilant 01, vowel/wide vowel 10      (signs 11: not sounds)
    varga     payload = place * 5 + member;  member = voiceless, +asp, voiced, +asp, nasal (the row edges)
    non-varga payload = place * 4 + slot;    place = the highest atom of the vertex's place on the spine
              K T M D O = 0 1 2 3 4;          slot = 0 voiceless fricative, 1 voiced fricative, 2 sonorant
    vowel     payload = row * 4 + nasal * 2 + long;  row from the place atoms: a=K i=T u=O ṛ=M ḷ=D e=K|T o=K|O;
              ai / au = the long form of the e / o row (the hand table's choice, class-10 spec 3.3)

Only the 42 sounds, the long vowels ā ī ū ṝ and the nasal vowels are covered. Signs, the Ukrainian
extension cells and `ḹ` (no such sound, Kasika txt 389) are out of scope here.
"""

from __future__ import annotations

import csv
import os
from typing import Dict, Tuple

import upc14v2 as g
import upc14v2_sandhi as sd

HERE = os.path.dirname(__file__)
S = g.SOUNDS

CLASS_VARGA, CLASS_NONVARGA, CLASS_VOWEL = 0b00, 0b01, 0b10
SPINE = {g.K: 0, g.T: 1, g.M: 2, g.D: 3, g.O: 4}
VOWEL_ROW = {g.K: 0, g.T: 1, g.O: 2, g.M: 3, g.D: 4, g.K | g.T: 5, g.K | g.O: 6}


class DeriveError(ValueError):
    pass


def derive(code: int) -> int:
    """The UPC-7 cell (7 bits) of a UPC-14 vertex, by the rules above."""
    v = g.unpack(code)
    if v.aperture == g.STOP:
        place = SPINE[v.place]
        if v.nasal:
            member = 4
        else:
            member = (2 if v.voice else 0) + (1 if v.asp else 0)
        return CLASS_VARGA << 5 | (place * 5 + member)
    if v.aperture in (g.SEMIVOWEL, g.SIBILANT):
        top = max(a for a in SPINE if v.place & a)
        if v.aperture == g.SEMIVOWEL:
            slot = 2
        else:
            slot = 1 if v.voice else 0
        return CLASS_NONVARGA << 5 | (SPINE[top] * 4 + slot)
    if v.length == g.PLUTA:
        raise DeriveError(f"{g.bits(code)} is a pluta vowel: the 7-bit cells have no pluta")
    row = VOWEL_ROW.get(v.place)
    if row is None:
        raise DeriveError(f"{g.bits(code)} has no vowel row")
    long_bit = 1 if (v.length == g.LONG and row < 5) or v.aperture == g.WIDE_VOWEL else 0
    return CLASS_VOWEL << 5 | (row * 4 + v.nasal * 2 + long_bit)


def placed_cells() -> Dict[str, int]:
    """IAST spelling -> the cell the hand design placed for it (from upc7-table.tsv)."""
    out: Dict[str, int] = {}
    with open(os.path.join(HERE, "upc7-table.tsv"), encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["status"] == "assigned" and row["sa-iast"]:
                out[row["sa-iast"]] = int(row["bits"], 2)
    return out


def compare() -> Tuple[list, list, list]:
    """(agree, differ, missing): sounds checked against the hand-placed table."""
    placed = placed_cells()
    names = list(S) + ["ā", "ī", "ū", "ṝ"]
    agree, differ, missing = [], [], []
    for name in names:
        cell = derive(sd.code_of(name))
        if name not in placed:
            missing.append((name, cell))
        elif placed[name] == cell:
            agree.append(name)
        else:
            differ.append((name, cell, placed[name]))
    return agree, differ, missing


if __name__ == "__main__":
    agree, differ, missing = compare()
    print(f"agree {len(agree)}, differ {len(differ)}, not in the table {len(missing)}")
    for name, derived, hand in differ:
        print(f"  {name:>3}: derived {derived:07b}  hand-placed {hand:07b}")
    for name, derived in missing:
        print(f"  {name:>3}: derived {derived:07b}  (no placed cell)")
