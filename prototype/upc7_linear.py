#!/usr/bin/env python3
"""Is there a GF(2)-LINEAR 7-bit cell for the Sanskrit sounds? (research, hypothesis; not a table proposal)

Question: cell = M . vertex (a 7x14 matrix over GF(2)) so that an edge that is an XOR on the 14-bit code (asp, voice, long
at a given length) is the SAME XOR on every cell? The hand-placed UPC-7 table cannot (place*5+member is mixed radix:
asp is +1, voice +2, not an XOR; see upc14v2_bitops.xor_masks_of_pairs).

Result of `search()` (seeded random search, 300000 matrices, seed 3): the matrix below is injective on the 59 Sanskrit
sound vertices, and the edges asp, voice, long each have ONE XOR delta over all their pairs; nasal has 5.
Limits: the cells are NOT the pinned/hand table's cells; there is no class prefix; only the 59 images are valid (decode is a
lookup, fail-closed); join/shift/lift are not linear; the language layer is not built on it.
"""
import random
from typing import List, Optional

import upc14v2 as g
import upc7_lang as L

ROWS = [0x2939, 0x125B, 0x2B10, 0x00D8, 0x162E, 0x033C, 0x14BF]


def vertices() -> List[int]:
    return sorted(set(L.VERTEX_OF_CELL.values()))


def image(rows: List[int], code: int) -> int:
    y = 0
    for i, r in enumerate(rows):
        y |= (bin(r & code).count("1") & 1) << i
    return y


def deltas(rows: List[int], edge) -> set:
    vs = set(vertices())
    out = set()
    for c in vs:
        try:
            r = edge(c)
        except Exception:
            continue
        if r in vs:
            out.add(image(rows, c) ^ image(rows, r))
    return out


def score(rows: List[int]) -> Optional[int]:
    vs = vertices()
    if len({image(rows, c) for c in vs}) < len(vs):
        return None
    return sum(len(deltas(rows, e)) for e in (g.e_asp, g.e_voice, g.e_nasal, g.e_long))


def search(seed: int = 3, n: int = 300000):
    rng = random.Random(seed)
    best = (10 ** 9, None)
    for _ in range(n):
        rows = [rng.getrandbits(14) for _ in range(7)]
        s = score(rows)
        if s is not None and s < best[0]:
            best = (s, rows)
    return best


if __name__ == "__main__":
    print(search())
