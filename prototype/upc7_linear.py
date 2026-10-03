#!/usr/bin/env python3
"""Is there a GF(2)-LINEAR 7-bit cell for the Sanskrit sounds? (research, hypothesis; not a table proposal)

Question: cell = M . vertex (a 7x14 matrix over GF(2)) so that an edge that is an XOR on the 14-bit code (asp, voice, long
at a given length) is the SAME XOR on every cell? The hand-placed UPC-7 table cannot (place*5+member is mixed radix:
asp is +1, voice +2, not an XOR; see upc14v2_bitops.xor_masks_of_pairs).

Correction (shiva's review of #84): "asp, voice, long are each ONE XOR delta" is a TAUTOLOGY for any GF(2)-linear M, because
the 14-bit edge is c ^ m (masks 0x1, 0x2, 0x4 on all 59 vertices) and M.c ^ M.(c^m) = M.m. It is not a finding.
What is non-trivial here:
  (a) a linear 7x14 map injective on the 59 Sanskrit sound vertices EXISTS (rare: ~0.015% of random matrices);
  (b) nasal is set/clear, not flip: its 14-bit masks c^r differ, so it is one delta only if M happens to collapse them
      (this M: 5 deltas; whether some injective M gives 1 is OPEN, not shown either way);
  (c) the hand table cannot be linear (place*5+member is mixed radix).
Limits: the cells are NOT the pinned/hand table's cells; no class prefix; only the 59 images are valid (decode is a lookup,
fail-closed); join/shift/lift are not linear; the language layer is not built on it.
"""
import random
from typing import List

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


def is_injective(rows: List[int]) -> bool:
    vs = vertices()
    return len({image(rows, c) for c in vs}) == len(vs)


def search(seed: int = 3, n: int = 20000):
    """(number of injective matrices among n random ones, the first one). The search looks for injectivity only."""
    rng = random.Random(seed)
    found, first = 0, None
    for _ in range(n):
        rows = [rng.getrandbits(14) for _ in range(7)]
        if is_injective(rows):
            found += 1
            first = first or rows
    return found, first


if __name__ == "__main__":
    print(search())
