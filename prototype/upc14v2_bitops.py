#!/usr/bin/env python3
"""Every typed edge of the UPC-14 sound graph is ONE machine operation on the 14-bit code (research, hypothesis).

SENS's strongest positive result is that appending one bit to a CAR/CDR word is an executable composition step
(`...0` = CAR, `...1` = CDR). This module states the same kind of law for the sound domain and checks it
exhaustively:

    asp     the code with bit 0 flipped                    (xor 0x0001)   a stop <-> its aspirate
    voice   the code with bit 1 flipped                    (xor 0x0002)
    nasal   set the nose bit, voiced, unaspirated          (bit 7; | 0x0082, & ~1)
    shift   the place field moved one step along the spine (place << 1, bits 8..12)
    lift    the aperture field + n                         (+ n * 16, bits 4..6)
    join    the union of two places                        (| atoms << 8)
    long    the length field + 1                           (+ 4, bits 2..3)

`bit_edge(name, code, ...)` is the bit-arithmetic form; the graph form is `upc14v2.e_*`. `agree_everywhere()` compares
them on all 16384 codes: on every vertex the results are equal (or both raise); the bit form also fails closed on a code that is
not a vertex, which the graph edge `e_voice` does not (it returns `code ^ 2` without validating).
The same laws do NOT hold on the cells of the hand-placed UPC-7 table (place*5 + member is not bit-aligned): see
`xor_masks_of_pairs`.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, Set, Tuple

import upc14v2 as g

PLACE_MASK = 0x1F00
ASP, VOICE, NASAL = 0x0001, 0x0002, 0x0080


def bit_asp(code: int) -> int:
    v = g.unpack(code)
    if v.aperture != g.STOP:
        raise g.InvalidCode("asp edge exists on stops only")
    return code ^ ASP


def bit_voice(code: int) -> int:
    g.unpack(code)
    return code ^ VOICE


def bit_nasal(code: int) -> int:
    g.unpack(code)
    return (code | NASAL | VOICE) & ~ASP


def bit_shift(code: int) -> int:
    v = g.unpack(code)
    if v.place & g.O:
        raise g.InvalidCode("shift past the end of the spine")
    return (code & ~PLACE_MASK) | ((code & PLACE_MASK) << 1)


def bit_lift(code: int, steps: int = 1) -> int:
    v = g.unpack(code)
    if v.aperture + steps > g.WIDE_VOWEL:
        raise g.InvalidCode("aperture lift past the end of the path")
    return code + (steps << 4)


def bit_join(code: int, atoms: int) -> int:
    g.unpack(code)
    return code | (atoms << 8)


def bit_long(code: int) -> int:
    v = g.unpack(code)
    if v.aperture < g.VOWEL:
        raise g.InvalidCode("only a vowel has length")
    return code + 4 if v.length < g.PLUTA else code


def _outcome(fn: Callable[[], int]) -> Tuple[str, Optional[int]]:
    try:
        return "ok", fn()
    except g.GraphError:
        return "raise", None


def is_vertex(code: int) -> bool:
    try:
        g.unpack(code)
        return True
    except g.GraphError:
        return False


def agree_everywhere() -> Dict[str, Tuple[int, int, int, int]]:
    """per edge, over all 2^14 codes: (vertices, equal outcomes on vertices, non-vertex codes, non-vertex codes the GRAPH edge accepts).

    On a vertex the graph edge and the bit form must give the same result or both raise. On a code that is not a
    vertex the bit form fails closed; the last number counts the codes on which the graph edge does NOT (it returns a
    code without validating its input).
    """
    pairs = {
        "asp": (g.e_asp, bit_asp), "voice": (g.e_voice, bit_voice), "nasal": (g.e_nasal, bit_nasal),
        "shift": (g.e_shift, bit_shift), "lift1": (lambda c: g.e_lift(c, 1), lambda c: bit_lift(c, 1)),
        "lift3": (lambda c: g.e_lift(c, 3), lambda c: bit_lift(c, 3)), "long": (g.e_long, bit_long),
        "join K": (lambda c: g.e_join(c, g.K), lambda c: bit_join(c, g.K)),
        "join O": (lambda c: g.e_join(c, g.O), lambda c: bit_join(c, g.O)),
    }
    vertices = [c for c in range(1 << g.WIDTH) if is_vertex(c)]
    others = [c for c in range(1 << g.WIDTH) if not is_vertex(c)]
    out = {}
    for name, (graph_edge, bit_form) in pairs.items():
        equal = sum(1 for c in vertices if _outcome(lambda: graph_edge(c)) == _outcome(lambda: bit_form(c)))
        leaks = sum(1 for c in others if _outcome(lambda: graph_edge(c))[0] == "ok")
        out[name] = (len(vertices), equal, len(others), leaks)
    return out


def xor_masks_of_pairs(pairs: List[Tuple[int, int]]) -> Set[int]:
    """The set of `a ^ b` over pairs of cells: a bit flip is a law only if this set is one value."""
    return {a ^ b for a, b in pairs}


if __name__ == "__main__":
    for name, (vertices, equal, others, leaks) in agree_everywhere().items():
        print(f"{name:8} vertices {vertices}  equal {equal}  non-vertex codes {others}  accepted by the graph edge {leaks}")
