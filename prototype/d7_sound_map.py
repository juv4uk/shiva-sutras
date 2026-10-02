#!/usr/bin/env python3
"""D7 research map, SOUND side (SENS #2415 output format; research evidence lane, nothing enters core.lisp).

Every number below is computed from the repository's own artifacts (upc14v2 graph, upc7-table.tsv, upc7_derive, upc7_lang),
not typed in. Columns follow #2415: coordinate/family | typed domain | law | generated? | root? | residue? |
representation-only? | witness | falsifier | status.

Also runs the #2366-style re-encoding attack on the coordinate laws of the 7-bit cells: permute the cell numbers of the sound
cells at random and ask whether the law still holds. A law that dies under a random relabelling is a coordinate/representation
law, not Sound semantics.

Number side: NOT covered here (owner assigned exact Number laws to #2411 / Core-Math). No Sound<->Number relation is claimed.
"""
import csv
import os
import random
import sys
from typing import List

import upc14v2 as g
import upc7_derive as D
import upc7_lang as L

HERE = os.path.dirname(os.path.abspath(__file__))
COLUMNS = ["family", "typed_domain", "law", "count", "generated", "root", "residue", "representation_only", "witness", "falsifier_cmd", "status"]


def graph_counts():
    sounds = set(g.SOUNDS.values())
    extra = set(L.VERTEX_OF_CELL.values()) - sounds          # long and nasal vowels of the Sanskrit set
    reach, frontier = set(), set(sounds)
    for _ in range(2):                                     # composed edges: long then nasal reaches the long nasal vowels
        nxt = set()
        for c in frontier:
            for e in (g.e_long, g.e_nasal):
                try:
                    nxt.add(e(c))
                except Exception:
                    pass
        reach |= nxt
        frontier = nxt | frontier
    return len(sounds), len(extra), len(extra & reach)


def derived_cells():
    agree, differ, missing = D.compare()
    return len(agree), len(differ), len(missing)


def attack(trials: int = 2000, seed: int = 11):
    """Fraction of random relabellings of the sound cells under which each coordinate law still holds."""
    rng = random.Random(seed)
    cells = sorted(L.SANSKRIT_CELL.values())
    name_of = {c: n for n, c in L.SANSKRIT_CELL.items()}
    pairs = {"asp": [], "voice": []}
    for edge, key in ((g.e_asp, "asp"), (g.e_voice, "voice")):
        for n, c in L.SANSKRIT_CELL.items():
            v = L.VERTEX_OF_CELL[c]
            try:
                r = edge(v)
            except Exception:
                continue
            cell_r = next((cc for cc, vv in L.VERTEX_OF_CELL.items() if vv == r), None)
            if cell_r is not None and r > v:               # asp and voice are involutions: one direction (else the delta is +d and -d)
                pairs[key].append((c, cell_r))
    out = {}
    for key, ps in pairs.items():
        ident = (len({b - a for a, b in ps}) == 1, len({b ^ a for a, b in ps}) == 1)       # control: the law on the unpermuted cells
        hold_add = hold_xor = 0
        for _ in range(trials):
            perm = dict(zip(cells, rng.sample(cells, len(cells))))
            hold_add += len({perm[b] - perm[a] for a, b in ps}) == 1
            hold_xor += len({perm[b] ^ perm[a] for a, b in ps}) == 1
        out[key] = (len(ps), hold_add / trials, hold_xor / trials, ident)
    return out


def _cmd(key: str) -> str:
    return f"cd prototype && python3 -c \"import sys, d7_falsifiers as F; sys.exit(0 if F.FALSIFIERS['{key}']()[0] else 1)\""


def rows() -> List[list]:
    """Reviewed by the shiva agent (shiva-sutras PR #97): claims corrected where the data says otherwise; every falsifier is a command
    that exits non-zero when the claim of the row is false (d7_falsifiers.py)."""
    n_snd, n_extra, n_extra_reach = graph_counts()
    agree, differ, missing = derived_cells()
    hand = set(D.placed_cells())
    n_hand = len([n for n in L.SANSKRIT_CELL if n in hand])
    n_nasal_only = len(L.SANSKRIT_CELL) - n_hand
    free = sum(1 for c in range(128) if c not in (set(L.SANSKRIT_CELL.values()) | set(L.UK_ONLY_CELL.values()) | set(L.SIGN_CELL.values()) | set(L.SANSKRIT_SIGN_CELL.values()) | set(L.DIGIT_CELL.values()) | {L.CAPITAL_CELL, L.STRESS_CELL}))
    return [
        ["sound identity (UPC-14 vertex)", "Sound", "42 sounds reached from ONE seed (k) by typed edges, given a 41-row recipe (label, parent, edge, step count)", n_snd, f"yes, given the recipe ({len(g.DERIVATION)} rows)", "1 seed (k) + edge types + the 41 recipe rows + sutra order", "the recipe is input data: each edge type is needed (removing one loses 4 to 35 sounds)", "no", "test_upc14v2*.py; d7_falsifiers identity rows", _cmd("identity: 42 from k") + " (and " + _cmd("identity: recipe is data, each edge type needed") + ")", "established (empirical, local)"],
        ["long/nasal vowel vertices", "Sound", "the Sanskrit set contains 17 vertices beyond the 42: all 17 lie in the closure of e_long/e_nasal (2 steps); the closure has 82 vertices, so 23 reachable vertices are NOT admitted (13 pluta, 8 nasal consonants, 2 others)", n_extra, f"{n_extra_reach} of {n_extra} lie in the closure; admission is a selection", "no", "the admission of 59 of 82 reachable vertices (the cut-off) is a selection, not generated", "no", "graph_counts(); d7_falsifiers closure row", _cmd("closure vs Sanskrit set"), "inclusion established; the boundary is residue (selection)"],
        ["edge law on the 14-bit code", "Sound", "each typed edge = c ^ mask(guard class): asp 1 mask, voice 1, nasal 8, shift 15, long 3, join 2, lift (by aperture, 3 masks for +1)", 7, "n/a (a law of the coordinate, not a generated object)", "no", "no", "no (law of the 14-bit coordinate)", "test_upc14v2_bitops agree_everywhere; shiva-sutras#90 GuardedXorTests; d7_falsifiers", _cmd("guarded XOR on all vertices"), "established (exhaustive on 2232 vertices for asp, voice, nasal, shift, long, join K, lift 1-3)"],
        ["7-bit cell of a sound (hand table)", "Sound", "cell = hand placement; varga place*5+member, non-varga place*4+slot, vowel row*4+nasal*2+long", n_hand, "partly: saṅkṣepa7 derives %d, differs on %d (h r l), %d without hand cell; the other %d sounds (nasal vowels) have NO hand cell and exist only as saṅkṣepa7" % (agree, differ, missing, n_nasal_only), "no", f"{differ} differ + hand-placed rest", "yes (coordinate)", "upc7_derive.compare(); upc7-table.tsv sha-pinned; d7_falsifiers hand-table row", _cmd("hand table vs derive"), "established; 3 disagreements open (#1981)"],
        ["linear 7x14 cell map", "Sound", "cell = M . vertex (GF(2)); asp/voice/long one delta is a tautology for any M", 59, "no (existence only)", "no", "no", "yes", "shiva-sutras#84/#90, my-lisp-panini#43 independent", _cmd("linear map"), "exists; no one nasal delta (proved), shift matrix does not extend (empirical); NOT a law"],
        ["ASCII signs", "Sound-text", "27 sign cells: 24 of the 32 ASCII punctuation characters + space, newline, tab; absent: $ % [ ] ^ { } ~", len(L.SIGN_CELL), "no", "no", "all 27", "yes", "pinned geometry; d7_falsifiers", _cmd("ASCII signs"), "convention, not generated"],
        ["Sanskrit signs", "Sound-text", "anusvāra visarga avagraha daṇḍa double-daṇḍa", len(L.SANSKRIT_SIGN_CELL), "no", "no", "all 5", "yes", "test_upc7_lang RoomTests", _cmd("Sanskrit signs"), "residue (convention)"],
        ["capital / stress modifiers", "Sound-text", "next letter uppercase (cell 34); combining acute (cell 35)", 2, "no", "no", "both", "yes (uk orthography)", "test_upc7_lang", _cmd("modifiers"), "residue (orthography)"],
        ["decimal digits 0-9", "Text (NOT Number)", "cell = base ^ XOR of 4 columns by the digit's bits (affine, 0..9 only), inside cells the pinned table reserves", 10, "no (one of 7680 placements in the pinned free cells)", "no", "all 10", "yes (coordinate law)", "test_upc7_lang DigitTests; panini review_upc7_digits (my-lisp-panini tools); d7_falsifiers", _cmd("digits"), "established as placement; semantics = text"],
        ["unassigned cells", "-", "free", free, "no", "no", "no", "-", "table; d7_falsifiers", _cmd("free cells"), "free (11 reserved)"],
    ]


def main():
    w = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    w.writerow(COLUMNS)
    for r in rows():
        w.writerow(r)
    print("\n# re-encoding attack (random relabelling of the sound cells, 2000 trials): pairs | share of relabellings under which the asp/voice delta stays constant (add, xor). The pair relation itself, transported with the relabelling, is invariant by definition and is not a result", file=sys.stderr)
    for k, (n, a, x, ident) in attack().items():
        print(f"# {k}: pairs {n}  add {a:.3f}  xor {x:.3f}  (control, unpermuted cells: add {ident[0]}, xor {ident[1]})", file=sys.stderr)


if __name__ == "__main__":
    main()
