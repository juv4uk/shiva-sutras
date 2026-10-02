#!/usr/bin/env python3
"""Runnable falsifiers and the position-permutation attack for the D7 sound map (SENS #2415; research, hypothesis).

Every function returns (ok, detail). `python3 d7_falsifiers.py` prints one line per row and exits 1 when a claim of the map is FALSE.
Written by the shiva agent as the review of shiva-sutras PR #97.
"""
import itertools
import random
import sys
from collections import Counter
from typing import Callable, Dict, List, Tuple

import upc14v2 as g
import upc7_derive as D
import upc7_lang as L

Result = Tuple[bool, str]
def _try(fn, *a):
    try:
        return fn(*a)
    except Exception as exc:                      # noqa: BLE001
        return exc


VERTICES = [c for c in range(1 << g.WIDTH) if not isinstance(_try(g.unpack, c), Exception)]


# ---- row 1: identity from one seed + the recipe ---------------------------------------------------------------------
def f_identity() -> Result:
    reached, changed = {"k"}, True
    while changed:
        changed = False
        for label, parent, _edge in g.DERIVATION:
            if label not in reached and all(p in reached for p in parent.split("+") if p in g.SOUNDS):
                reached.add(label)
                changed = True
    ok = reached == set(g.SOUNDS) and len(g.DERIVATION) == 41
    return ok, f"reached {len(reached)} of {len(g.SOUNDS)} from k by {len(g.DERIVATION)} recipe rows; edge instances {dict(Counter(e for _, _, e in g.DERIVATION))}"


def f_identity_recipe_is_input() -> Result:
    """The recipe (label, parent, edge, step count) is DATA: 41 rows. Dropping any edge type loses sounds (each type is needed)."""
    lost = {}
    for edge in {e.split("+")[0] for _, _, e in g.DERIVATION}:
        reached, changed = {"k"}, True
        while changed:
            changed = False
            for label, parent, e in g.DERIVATION:
                if e.split("+")[0] == edge:
                    continue
                if label not in reached and all(p in reached for p in parent.split("+") if p in g.SOUNDS):
                    reached.add(label)
                    changed = True
        lost[edge] = len(g.SOUNDS) - len(reached)
    return all(v > 0 for v in lost.values()), f"sounds lost when an edge type is removed: {lost}"


# ---- row 2: the Sanskrit vowel set vs the edge closure ----------------------------------------------------------------
def closure() -> set:
    sounds = set(g.SOUNDS.values())
    reach, frontier = set(), set(sounds)
    for _ in range(2):
        nxt = set()
        for c in frontier:
            for e in (g.e_long, g.e_nasal):
                r = _try(e, c)
                if not isinstance(r, Exception):
                    nxt.add(r)
        reach |= nxt
        frontier = nxt | frontier
    return reach | sounds


def f_closure() -> Result:
    cl, sk = closure(), set(L.VERTEX_OF_CELL.values())
    over = cl - sk
    kinds = Counter(("pluta" if g.unpack(c).length == g.PLUTA else "nasal consonant" if g.unpack(c).aperture in (g.SEMIVOWEL, g.SIBILANT) else "other") for c in over)
    return sk <= cl, f"closure {len(cl)}, Sanskrit set {len(sk)}, in the set but not the closure {len(sk - cl)}, in the closure but not the set (selection, not generation) {len(over)}: {dict(kinds)}"


# ---- row 3: guarded XOR on all 2232 vertices ------------------------------------------------------------------------
def f_guarded_xor() -> Result:
    bad = Counter()
    for c in VERTICES:
        place = (c >> 8) & 0x1F
        forms = {
            "asp": (g.e_asp, lambda c: c ^ 1),
            "voice": (g.e_voice, lambda c: c ^ 2),
            "nasal": (g.e_nasal, lambda c: c ^ (((~c) & 0x82) | (c & 1))),
            "shift": (g.e_shift, lambda c: c ^ ((place ^ (place << 1)) << 8)),
            "long": (g.e_long, lambda c: c ^ (0 if ((c >> 2) & 3) == g.PLUTA else (4 if ((c >> 2) & 3) == 0 else 12))),
            "join K": (lambda c: g.e_join(c, g.K), lambda c: c ^ ((g.K & ~place) << 8)),
        }
        for n in (1, 2, 3):
            forms[f"lift{n}"] = ((lambda c, n=n: g.e_lift(c, n)), (lambda c, n=n: c ^ ((((c >> 4) & 7) ^ (((c >> 4) & 7) + n)) << 4)))
        for name, (edge, form) in forms.items():
            r = _try(edge, c)
            if isinstance(r, Exception):
                continue
            bad[name] += r != form(c)
    return not any(bad.values()), f"edge forms checked on {len(VERTICES)} vertices (asp, voice, nasal, shift, long, join K, lift1-3); mismatches {dict(bad)}"


# ---- row 4: the 7-bit cell of a sound ---------------------------------------------------------------------------------
def f_hand_table() -> Result:
    agree, differ, missing = D.compare()
    hand = set(D.placed_cells())
    in_table = [n for n in L.SANSKRIT_CELL if n in hand]
    nasal_only = [n for n in L.SANSKRIT_CELL if n not in hand]
    ok = (len(agree), len(differ), len(missing)) == (43, 3, 0) and len(in_table) == 46 and len(nasal_only) == 13
    return ok, f"hand-placed cells {len(in_table)} of the {len(L.SANSKRIT_CELL)} sounds; the other {len(nasal_only)} (nasal vowels) have NO hand cell (saṅkṣepa7 only); derive vs hand: {len(agree)} agree, {len(differ)} differ, {len(missing)} missing"


# ---- row 5: linear map ------------------------------------------------------------------------------------------------
def f_linear() -> Result:
    import upc7_linear as X
    import upc7_linear_ext as E
    ok = X.is_injective(X.ROWS) and len(X.deltas(X.ROWS, g.e_nasal) - {0}) == 4 and not E.affine_T_exists(E.SHIFT_ROWS, [(c, g.e_shift(c)) for c in E.all_vertices() if not g.unpack(c).place & g.O])
    return ok, "an injective M exists; nasal has 4 nonzero deltas; the shift matrix does not extend to the 1080 shift pairs"


# ---- rows 6-8: signs and modifiers ------------------------------------------------------------------------------------
def f_ascii_signs() -> Result:
    punct = [chr(i) for i in range(33, 127) if not chr(i).isalnum()]
    covered = [ch for ch in punct if ch in L.SIGN_CELL]
    other = [k for k in L.SIGN_CELL if k not in punct]
    missing = [ch for ch in punct if ch not in L.SIGN_CELL]
    ok = len(L.SIGN_CELL) == 27 and len(covered) == 24 and sorted(other) == sorted([" ", "\n", "\t"])
    return ok, f"27 sign cells = {len(covered)} of the 32 ASCII punctuation characters + {len(other)} whitespace; absent: {''.join(missing)}"


def f_sanskrit_signs() -> Result:
    return sorted(L.SANSKRIT_SIGN_CELL) == sorted(["anusvara", "visarga", "avagraha", "danda", "double-danda"]), f"{sorted(L.SANSKRIT_SIGN_CELL)}"


def f_modifiers() -> Result:
    others = set(L.SANSKRIT_CELL.values()) | set(L.SIGN_CELL.values()) | set(L.DIGIT_CELL.values()) | set(L.SANSKRIT_SIGN_CELL.values())
    return L.CAPITAL_CELL != L.STRESS_CELL and not ({L.CAPITAL_CELL, L.STRESS_CELL} & others), f"capital {L.CAPITAL_CELL}, stress {L.STRESS_CELL}, claimed by nothing else"


# ---- row 9: digits ----------------------------------------------------------------------------------------------------
def f_digits() -> Result:
    import upc7_digits_compare as DC
    cells = [L.DIGIT_CELL[str(d)] for d in range(10)]
    dec = DC.affine_decoder(cells)
    value_ok = dec is not None and all(sum(((bin(w & c).count("1") & 1) ^ b) << i for i, (w, b) in enumerate(dec)) == d for d, c in enumerate(cells))
    return value_ok and not (set(cells) & DC.pinned_assigned()), f"digit value from the cell by bit operations {dec}; no cell of the pinned table is used"


def f_free() -> Result:
    claimed = set(L.SANSKRIT_CELL.values()) | set(L.UK_ONLY_CELL.values()) | set(L.SIGN_CELL.values()) | set(L.SANSKRIT_SIGN_CELL.values()) | set(L.DIGIT_CELL.values()) | {L.CAPITAL_CELL, L.STRESS_CELL}
    free = [c for c in range(128) if c not in claimed]
    return len(free) == 11, f"free cells {free}"


def f_position_attack() -> Result:
    """The claim of the symmetry row: the row-internal laws survive any permutation of whole rows (places); the order law (shift) does not."""
    r = attack_positions()
    asp = r["asp (pairs 10) under places permutations"]["constant add delta"]
    voice = r["voice (pairs 10) under places permutations"]["constant add delta"]
    shift = r["shift (pairs 20) under places permutations"]["constant add delta"]
    sav = r["savarṇa row relation (same place <=> same cell // 5) under place permutations"]["holds"]
    return (asp, voice, sav, shift) == (120, 120, 120, 2), f"survive of 120 place permutations: asp {asp}, voice {voice}, row relation {sav}; shift (order of places) {shift}"


FALSIFIERS: Dict[str, Callable[[], Result]] = {
    "identity: 42 from k": f_identity, "identity: recipe is data, each edge type needed": f_identity_recipe_is_input,
    "closure vs Sanskrit set": f_closure, "guarded XOR on all vertices": f_guarded_xor, "hand table vs derive": f_hand_table,
    "linear map": f_linear, "ASCII signs": f_ascii_signs, "Sanskrit signs": f_sanskrit_signs, "modifiers": f_modifiers,
    "digits": f_digits, "free cells": f_free, "position attack": f_position_attack,
}


# ---- the position-permutation attack ----------------------------------------------------------------------------------
def stop_cells() -> Dict[str, Tuple[int, int]]:
    """stop name -> (place index 0..4, member 0..4) read from the saṅkṣepa7 cell (place*5 + member)."""
    out = {}
    for name, cell in L.SANSKRIT_CELL.items():
        if cell >> 5 == 0:
            out[name] = ((cell & 31) // 5, (cell & 31) % 5)
    return out


def stop_pairs(edge) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    st = stop_cells()
    by_vertex = {L.SANSKRIT_VERTEX[n]: pm for n, pm in st.items()}
    out = []
    for v, pm in by_vertex.items():
        r = _try(edge, v)
        if not isinstance(r, Exception) and r in by_vertex and r != v:
            if edge in (g.e_asp, g.e_voice) and r < v:                  # an involution: take one direction (unaspirated -> aspirated, voiceless -> voiced)
                continue
            out.append((pm, by_vertex[r]))
    return out


def attack_positions() -> Dict[str, Dict[str, int]]:
    """Permute the ROWS (places) or the COLUMNS (members) of the varga block: cell = sigma_p(place)*5 + sigma_m(member).
    For each law, count the permutations (of 120 each) under which it still holds: an additive/xor constant delta of an edge, and the
    row relation 'same place <=> same row'. A law that survives every permutation is structural; one that survives few is arithmetic."""
    perms = list(itertools.permutations(range(5)))
    edges = {"asp": g.e_asp, "voice": g.e_voice, "nasal": g.e_nasal, "shift": g.e_shift}
    pairs = {k: stop_pairs(e) for k, e in edges.items()}
    res: Dict[str, Dict[str, int]] = {}
    for kind in ("members", "places"):
        for name, ps in pairs.items():
            add = xor = 0
            for sig in perms:
                def cell(pm, sig=sig):
                    p, m = pm
                    return (p * 5 + sig[m]) if kind == "members" else (sig[p] * 5 + m)
                add += len({cell(b) - cell(a) for a, b in ps}) == 1
                xor += len({cell(b) ^ cell(a) for a, b in ps}) == 1
            res.setdefault(f"{name} (pairs {len(ps)}) under {kind} permutations", {"constant add delta": add, "constant xor delta": xor, "of": len(perms)})
    st = stop_cells()
    keep = 0
    for sig in perms:
        keep += all(((sig[p1] * 5 + m1) // 5 == (sig[p2] * 5 + m2) // 5) == (p1 == p2) for (p1, m1), (p2, m2) in itertools.product(st.values(), repeat=2))
    res["savarṇa row relation (same place <=> same cell // 5) under place permutations"] = {"holds": keep, "of": len(perms)}
    return res


def attack_bit_positions(trials: int = 300, seed: int = 5) -> Dict[str, int]:
    """Control: permute the BIT POSITIONS of the 14-bit code (not the cells). Each of asp, voice stays one constant xor mask."""
    rng = random.Random(seed)
    out = {"asp": 0, "voice": 0}
    for _ in range(trials):
        perm = list(range(14))
        rng.shuffle(perm)

        def p(c):
            return sum(((c >> i) & 1) << perm[i] for i in range(14))
        for name, edge in (("asp", g.e_asp), ("voice", g.e_voice)):
            masks = set()
            for c in VERTICES:
                r = _try(edge, c)
                if not isinstance(r, Exception):
                    masks.add(p(c) ^ p(r))
            out[name] += len(masks) == 1
    out["of"] = trials
    return out


def main() -> int:
    failed = 0
    for name, fn in FALSIFIERS.items():
        ok, detail = fn()
        failed += not ok
        print(f"{'OK  ' if ok else 'FAIL'}\t{name}\t{detail}")
    print("# position-permutation attack on the varga block (cell = place*5 + member):")
    for k, v in attack_positions().items():
        print(f"#   {k}: {v}")
    print(f"# control, permuting the bit positions of the 14-bit code: {attack_bit_positions()}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
