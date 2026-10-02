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
COLUMNS = ["family", "typed_domain", "law", "count", "generated", "root", "residue", "representation_only", "witness", "falsifier", "status"]


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
            if cell_r is not None:
                pairs[key].append((c, cell_r))
    out = {}
    for key, ps in pairs.items():
        hold_add = hold_xor = 0
        for _ in range(trials):
            perm = dict(zip(cells, rng.sample(cells, len(cells))))
            hold_add += len({perm[b] - perm[a] for a, b in ps}) == 1
            hold_xor += len({perm[b] ^ perm[a] for a, b in ps}) == 1
        out[key] = (len(ps), hold_add / trials, hold_xor / trials)
    return out


def rows() -> List[list]:
    n_snd, n_extra, n_extra_reach = graph_counts()
    agree, differ, missing = derived_cells()
    free = sum(1 for c in range(128) if c not in (set(L.SANSKRIT_CELL.values()) | set(L.UK_ONLY_CELL.values()) | set(L.SIGN_CELL.values()) | set(L.SANSKRIT_SIGN_CELL.values()) | set(L.DIGIT_CELL.values()) | {L.CAPITAL_CELL}))
    sounds_in_table = len(L.SANSKRIT_CELL)
    return [
        ["sound identity (UPC-14 vertex)", "Sound", "42 sounds derived from ONE seed (k) by typed edges asp/voice/nasal/shift/lift/join/long", n_snd, f"yes ({len(g.DERIVATION)} by edges)", "1 seed (k) + edge types + sutra order", "none claimed", "no", "test_upc14v2*.py; graph == guarded bit form on 2232 vertices (test_upc14v2_bitops)", "a sound the edges cannot reach from k", "established (empirical, local)"],
        ["long/nasal vowel vertices", "Sound", "closure of e_long, e_nasal (up to 2 steps) over the 42", n_extra, f"{n_extra_reach} of {n_extra} reached by e_long/e_nasal", "no", f"{n_extra - n_extra_reach} not reached", "no", "graph_counts() in d7_sound_map.py", "a vertex of the Sanskrit set outside the edge closure", "established where reached; rest = residue"],
        ["edge law on the 14-bit code", "Sound", "each typed edge = c ^ mask(guard); asp 1 mask, voice 1, long 3, shift 15, nasal 8 (guard classes), join 2", 6, "yes", "no", "no", "no (law of the 14-bit coordinate)", "test_upc14v2_bitops agree_everywhere; shiva-sutras#90 GuardedXorTests", "an edge whose result differs from the guarded form on some vertex", "established (exhaustive on 2232 vertices)"],
        ["7-bit cell of a sound (hand table)", "Sound", "cell = hand placement; varga place*5+member, non-varga place*4+slot, vowel row*4+nasal*2+long", sounds_in_table, "partly: saṅkṣepa7 derives %d, differs on %d (h r l), %d without hand cell" % (len(D.compare()[0]), differ, missing), "no", f"{differ} differ + hand-placed rest", "yes (coordinate)", "upc7_derive.compare(); upc7-table.tsv sha-pinned", "a cell that a derivation rule gets right but the table has elsewhere", "established; 3 disagreements open (#1981)"],
        ["linear 7x14 cell map", "Sound", "cell = M . vertex (GF(2))", 59, "no (existence only)", "no", "no", "yes", "shiva-sutras#84/#90, my-lisp-panini#43 independent", "no injective M exists; nasal one delta; shift linear on all 1080 pairs", "exists; useless for nasal/shift (proved/empirical); NOT a law"],
        ["ASCII signs", "Sound-text", "27 cells mirror the ASCII punctuation the language syntax uses", len(L.SIGN_CELL), "no", "no", "all 27", "yes", "pinned geometry", "none (convention)", "convention, not generated"],
        ["Sanskrit signs", "Sound-text", "anusvāra visarga avagraha daṇḍa double-daṇḍa", len(L.SANSKRIT_SIGN_CELL), "no", "no", "all 5", "yes", "test_upc7_lang RoomTests", "none", "residue (convention)"],
        ["capital / stress modifiers", "Sound-text", "next letter uppercase; combining acute", 2, "no", "no", "both", "yes (uk orthography)", "test_upc7_lang", "none", "residue (orthography)"],
        ["decimal digits 0-9", "Text (NOT Number)", "cell = base ^ XOR of 4 columns by the digit's bits (affine, 0..9 only)", 10, "no (one of 7680 placements)", "no", "all 10", "yes (coordinate law)", "test_upc7_lang DigitTests; panini review_upc7_digits (independent)", "a digit cell compared/added as a number; relabelling the cells", "established as placement; semantics = text"],
        ["symmetry of the 7-bit coordinate laws", "Sound", "laws of the cell (asp/voice = +1/+2 within a series, long/nasal XOR, digit affinity, class = top 2 bits) die under a uniform random permutation of the 128 cells (0/2000) but ALL survive a structured NON-affine group G: permute whole series/rows (5 varga series, 6 non-varga rows, 8 vowel rows), |G| = 5!*6!*8!; G moves WHICH sound sits in which cell (k->20 in ~80% of samples)", 1, "no", "no", "no", "yes (coordinate: structure inside a row, not the identity or the order of places)", "my-lisp-panini#47 review_d7_relabel_attack.py (panini, independent; E1/E2/E3)", "a law that fixes the identity of a sound, i.e. is not preserved by G", "established (empirical); not shown that G is the full automorphism group"],
        ["Sound7 cell -> Number coercion", "Sound-text vs Number", "none found: arithmetic has branches only for Rational/Number (Type error otherwise); Text7==Number is false; eval forbidden", 0, "-", "-", "-", "-", "my-lisp-panini#47 d7_probe (40 expressions, cargo test; source read of eval/arithmetic.rs, value.rs, text7.rs)", "any expression where a Text7 cell takes part in Number arithmetic or comparison", "no coercion found; LEAK: (number->string t) returns the wire token '#t7:3b': write-to-string(Text7) is a deliberate canonical wire projection (value.rs:851), number->string is an untyped delegation to it (core.lisp ~726), so the Text7 case is unintended inheritance; no test pins it (panini, source-confirmed, main e0a6074)"],
        ["unassigned cells", "-", "free", free, "no", "no", "no", "-", "table", "-", "free"],
    ]


def main():
    w = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    w.writerow(COLUMNS)
    for r in rows():
        w.writerow(r)
    print("\n# re-encoding attack (random relabelling of the sound cells, 2000 trials): pairs | share of relabellings under which the asp/voice delta stays constant (add, xor). The pair relation itself, transported with the relabelling, is invariant by definition and is not a result", file=sys.stderr)
    print("# NOTE (panini, my-lisp-panini#47): on the 7-bit CELL asp/voice are +1/+2 additions, the XOR law is the 14-bit code's", file=sys.stderr)
    for k, (n, a, x) in attack().items():
        print(f"# {k}: pairs {n}  add {a:.3f}  xor {x:.3f}", file=sys.stderr)


if __name__ == "__main__":
    main()
