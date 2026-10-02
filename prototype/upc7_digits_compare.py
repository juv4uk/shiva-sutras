#!/usr/bin/env python3
"""Two placements of the ten text digits in the free cells, compared on the requirements of shiva-sutras#34 (research, hypothesis).

Candidates (cells of the digits 0..9):
  affine-v3        the one merged in PR #93: cell = base ^ XOR of 4 columns by the digit's bits, in the free cells of the v3 candidate
                   (the candidate that moved h, r, l)
  ordinal-v3       the first ten free cells of the v3 candidate in numeric order
  ordinal-pinned   the first ten free cells of the PINNED table in numeric order
  affine-pinned    the best affine embedding in the free cells of the PINNED table (most cells in the varga class)

The pinned `upc7-table.tsv` is read only. Run `python3 upc7_digits_compare.py` for the enumeration of affine embeddings (about a minute).
"""
import csv
import os
from typing import Dict, List, Optional, Tuple

import upc7_lang as L

HERE = os.path.dirname(os.path.abspath(__file__))

CLASS = {0: "varga", 1: "non-varga", 2: "vowel", 3: "sign"}


def pinned_assigned() -> set:
    with open(os.path.join(HERE, "upc7-table.tsv"), encoding="utf-8") as handle:
        return {int(r["bits"], 2) for r in csv.DictReader(handle, delimiter="\t") if r["status"] == "assigned"}


def v3_claimed_without_digits() -> set:
    claimed = set(L.SANSKRIT_CELL.values()) | set(L.UK_ONLY_CELL.values()) | set(L.SIGN_CELL.values()) | {L.CAPITAL_CELL}
    claimed |= set(getattr(L, "SANSKRIT_SIGN_CELL", {}).values())
    return claimed - set(L.DIGIT_CELL.values())


def free_cells(claimed: set) -> List[int]:
    return [c for c in range(128) if c not in claimed]


def free_v3() -> List[int]:
    return free_cells(v3_claimed_without_digits())


def free_pinned() -> List[int]:
    return free_cells(pinned_assigned())


# the best affine embedding in the PINNED free cells (6 varga + 4 non-varga), from `enumerate_affine`
AFFINE_PINNED = [28, 31, 29, 30, 56, 59, 57, 58, 25, 26]


def candidates() -> Dict[str, List[int]]:
    return {
        "affine-v3": [L.DIGIT_CELL[str(d)] for d in range(10)],
        "ordinal-v3": free_v3()[:10],
        "ordinal-pinned": free_pinned()[:10],
        "affine-pinned": list(AFFINE_PINNED),
    }


def affine_decoder(cells: List[int]) -> Optional[List[Tuple[int, int]]]:
    """For each digit bit: (mask w, constant b) with bit = parity(cell & w) ^ b on the ten cells, or None when the digit is not an
    affine function of the cell (then no bit operation gives the digit; a table or arithmetic is needed)."""
    out = []
    for bit in range(4):
        found = None
        for w in range(128):
            for b in (0, 1):
                if all(((bin(w & c).count("1") & 1) ^ b) == ((d >> bit) & 1) for d, c in enumerate(cells)):
                    found = (w, b)
                    break
            if found:
                break
        if found is None:
            return None
        out.append(found)
    return out


def metrics(cells: List[int]) -> dict:
    classes = [CLASS[c >> 5] for c in cells]
    return {
        "cells": cells,
        "varga": classes.count("varga"),
        "non-varga": classes.count("non-varga"),
        "vowel": classes.count("vowel"),
        "consecutive": all(cells[i + 1] - cells[i] == 1 for i in range(9)),
        "affine_decoder": affine_decoder(cells),
        "collides_with_pinned": sorted(set(cells) & pinned_assigned()),
    }


def enumerate_affine(free: List[int]) -> List[Tuple[int, Tuple[int, int, int, int], List[int]]]:
    """all (base, columns, cells) with cell(d) = base ^ XOR(columns by the bits of d) for d = 0..9, all ten in `free` and distinct."""
    fset, out = set(free), []
    for b in free:
        opts = [f ^ b for f in free if f != b]
        for c0 in opts:
            for c1 in opts:
                if c1 == c0:
                    continue
                for c2 in opts:
                    if c2 in (c0, c1, c0 ^ c1):
                        continue
                    for c3 in opts:
                        cols = (c0, c1, c2, c3)
                        cells = []
                        for d in range(10):
                            x = b
                            for i in range(4):
                                if (d >> i) & 1:
                                    x ^= cols[i]
                            cells.append(x)
                        if all(x in fset for x in cells) and len(set(cells)) == 10:
                            out.append((b, cols, cells))
    return out


if __name__ == "__main__":
    for name, cells in candidates().items():
        print(name, metrics(cells))
    for name, fr in (("v3 free (non-vowel)", [c for c in free_v3() if c >> 5 < 2]), ("pinned free", free_pinned())):
        print(name, len(fr), "affine embeddings:", len(enumerate_affine(fr)))
