#!/usr/bin/env python3
"""Extensions of the GF(2)-linear 7-bit cell (issue #85; research, hypothesis; proofs are exact, searches are seeded).

Results on the 59 Sanskrit vertices `upc7_linear.vertices()`:

 1. nasal. e_nasal pairs (c, c^r): the masks r are {0x80, 0x81, 0x82, 0x83} and the fixed point 0 (an already nasal vowel).
    ONE nonzero delta is IMPOSSIBLE for an injective linear M: it would need M.0x81 = M.0x82 = M.0x80 (hence M.0x1 = 0 and
    M.0x2 = 0), but then asp pairs (k, kh) collide. The four nonzero deltas are pairwise distinct for every injective M, so 4
    is the minimum. The "5 deltas" of #84 counted the trivial delta 0 of the 18 fixed points.
 2. class. Is the class (varga / non-varga / vowel) a function of fixed output bits? For a class indicator that is constant per
    class, only the patterns of `is_nonvarga` are affine on the 59 vertices: stop and vowel cannot be told apart by ANY affine
    bit (exact, `class_patterns`). A 2-bit class code that is constant on the stops (e.g. out = ap0^ap2, ap1^ap2) cannot be
    injective: the 25 stops need 5 bits for themselves and the member differences span GF(2)^3, which leaves a quotient with
    4 classes for 5 places (pigeonhole, `stop_quotient_classes`). A hill climb with the class bits fixed that way ended at 2
    collisions (200 restarts).
 3. shift, lift, join. `edge_pairs` and `affine_T_exists` ask for an affine T with T.M(c) + b = M(edge(c)). lift and join have
    7 to 10 pairs, so a T exists for almost any M (not a finding). shift has 36 pairs: of 25 random injective matrices 1 had an
    affine T; a seeded hill climb found an injective M with an affine T for shift (not a linear T: 120 restarts left 1 equation).
"""
import itertools
import random
from typing import Dict, List, Tuple

import upc14v2 as g
import upc7_linear as X

V = X.vertices()
VS = set(V)


def edge_pairs(edge, include_fixed: bool = False) -> List[Tuple[int, int]]:
    out = []
    for c in V:
        try:
            r = edge(c)
        except Exception:
            continue
        if r in VS and (include_fixed or r != c):
            out.append((c, r))
    return out


def nasal_masks() -> Dict[int, int]:
    counts: Dict[int, int] = {}
    for c, r in edge_pairs(g.e_nasal, include_fixed=True):
        counts[c ^ r] = counts.get(c ^ r, 0) + 1
    return counts


def class_of(code: int) -> int:
    ap = g.unpack(code).aperture
    return 0 if ap == g.STOP else (1 if ap in (g.SEMIVOWEL, g.SIBILANT) else 2)


def _consistent(equations) -> bool:
    basis: List[Tuple[int, int]] = []
    for m, t in equations:
        for bm, bt in basis:
            if m & (bm & -bm):
                m ^= bm
                t ^= bt
        if m == 0:
            if t:
                return False
        else:
            basis.append((m, t))
    return True


def class_patterns() -> Dict[Tuple[int, int, int], Tuple[bool, bool]]:
    """pattern (stop, non-varga, vowel) -> (linear on V, affine on V)."""
    out = {}
    for pat in itertools.product((0, 1), repeat=3):
        lin = _consistent([(c, pat[class_of(c)]) for c in V])
        aff = _consistent([(c | (1 << g.WIDTH), pat[class_of(c)]) for c in V])
        out[pat] = (lin, aff)
    return out


def stop_quotient_classes() -> Tuple[int, int]:
    """(places, classes of the quotient): the stop member differences span a space of dim d; an injective map into k bits leaves
    2**(k-d) classes for the places. Returns (number of stop places, 2**(5-d))."""
    stops = [c for c in V if g.unpack(c).aperture == g.STOP]
    member_mask = 0x0083
    members = {c & member_mask for c in stops}
    diffs = {a ^ b for a in members for b in members}
    span = {0}
    for d in diffs:
        span |= {s ^ d for s in span}
    d = len(span).bit_length() - 1
    places = {c & 0x1F00 for c in stops}
    return len(places), 2 ** (5 - d)


def affine_T_exists(rows: List[int], pairs: List[Tuple[int, int]], linear: bool = False) -> bool:
    xs = [(X.image(rows, c), X.image(rows, r)) for c, r in pairs]
    for out in range(7):
        eqs = [(x | ((0 if linear else 1) << 7), (y >> out) & 1) for x, y in xs]
        if not _consistent(eqs):
            return False
    return True


# ---- guarded XOR forms: every edge is c ^ mask(guard class of c), checked on all 2232 vertices -----------------------
def all_vertices() -> List[int]:
    out = []
    for c in range(1 << g.WIDTH):
        try:
            g.unpack(c)
        except g.GraphError:
            continue
        out.append(c)
    return out


def nasal_mask(c: int) -> int:
    """set the nose and voice bits, clear asp: a flip only where the bit is not yet in its target state. Guard class = (nasal, voice, asp)."""
    return ((~c) & 0x0082) | (c & 0x0001)


def join_mask(c: int, atoms: int) -> int:
    """OR of place atoms = XOR with the atoms not yet present. Guard class = which of `atoms` are already in the place."""
    return (atoms & ~((c >> 8) & 0x1F)) << 8


def long_mask(c: int) -> int:
    """length + 1 (saturating at pluta): 4 at length 0, 12 at length 1, 0 at pluta. Guard class = the length."""
    length = (c >> 2) & 3
    return 0 if length == g.PLUTA else (0x4 if length == 0 else 0xC)


def edge_mask_count(edge) -> Tuple[int, int, int]:
    """(vertices where the edge is defined, distinct masks c^edge(c), vertices where it is undefined) over ALL 2232 vertices."""
    masks, defined = set(), 0
    for c in all_vertices():
        try:
            masks.add(c ^ edge(c))
            defined += 1
        except g.GraphError:
            pass
    return defined, len(masks), len(all_vertices()) - defined


SHIFT_ROWS = [0x3BFD, 0x072A, 0x2D6F, 0x1CC2, 0x3218, 0x2897, 0x277A]    # seeded hill climb (seed 2): injective, affine T for shift


if __name__ == "__main__":
    print(nasal_masks(), class_patterns(), stop_quotient_classes())
