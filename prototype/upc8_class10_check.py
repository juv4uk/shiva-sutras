#!/usr/bin/env python3
"""UPC-8 Class 10 (vowels) — geometry validator.

Checks that every code is derivable from the field spec
[7:6]=10, [5:3]=row, [2]=free(0), [1]=nasal, [0]=length,
and that the pratyahara range predicates are exactly expressible.
"""
import sys

ROWS = ["a", "i", "u", "R", "L", "e", "o"]
LONG_MAP = {"a": "aa", "i": "ii", "u": "uu", "R": "RR", "L": "LL",
            "e": "ai", "o": "au"}

def code(row_idx: int, length: int = 0, nasal: int = 0, free: int = 0) -> int:
    return 0x80 | (row_idx << 3) | (free << 2) | (nasal << 1) | length

def main() -> int:
    failures = []
    table = []

    for r, row in enumerate(ROWS):
        for length in (0, 1):
            for nasal in (0, 1):
                c = code(r, length, nasal)
                glyph = LONG_MAP[row] if length else row
                if nasal:
                    glyph += "(n)"
                table.append((c, glyph, r, length, nasal))
                # invariant: class bits == 10
                if (c >> 6) != 0b10:
                    failures.append(f"class bits wrong: 0x{c:02X}")
                # invariant: free bit is 0 in protected Sanskrit layer
                if c & 0x04:
                    failures.append(f"free bit set: 0x{c:02X}")

    print("Row table (28 entries):")
    for c, glyph, r, ln, ns in table:
        print(f"  0x{c:02X}  {glyph:<6} row={r} len={ln} nas={ns}")

    # range predicates
    ac_14 = [code(r, l, 0) for r in range(7) for l in (0, 1)]   # all 14 vowels, nasal=0
    ac_9  = [code(r, 0, 0) for r in range(7)] + [0xA9, 0xB1]    # canonical 9 incl. ai, au
    aN  = [code(r, 0, 0) for r in range(5)]          # a i u R L  (sutra 1-2)
    ik  = [code(r, 0, 0) for r in range(1, 5)]       # i u R L

    print(f"\nac (14, nasal=0) = {[hex(c) for c in ac_14]}")
    print(f"ac (canonical 9)  = {[hex(c) for c in ac_9]}")
    print(f"aN  = {[hex(c) for c in aN]}  (count={len(aN)})")
    print(f"ik  = {[hex(c) for c in ik]}  (count={len(ik)})")

    # range predicate must be a simple interval on short codes
    def interval_ok(ls):
        return list(ls) == list(range(ls[0], ls[-1] + 1, 8))
    for name, pred in (("aN", aN), ("ik", ik)):
        ok = interval_ok(pred)
        print(f"  {name}: interval-with-step-8 -> {'OK' if ok else 'FAIL'}")
        if not ok:
            failures.append(f"{name} not interval")

    # ac as a bit predicate (nasal==0 & free==0) == exactly the 14.
    # GOTCHA: reserved row 7 (0xB8-0xBF) also has (c >> 6)==10 and low bits 0,
    # so the predicate MUST exclude row 7: (c & 0x38) != 0x38.
    naive_pred = [c for c in range(0x80, 0xC0)
                  if (c >> 6) == 0b10 and (c & 0x06) == 0]
    if 0xB8 in naive_pred:
        print("  gotcha confirmed: naive bit-predicate leaks reserved row 0xB8")
    bit_pred_ac = [c for c in naive_pred if (c & 0x38) != 0x38]
    if bit_pred_ac != ac_14:
        failures.append(f"bit-predicate ac mismatch: {[hex(c) for c in bit_pred_ac]} != {[hex(c) for c in ac_14]}")
    print(f"  ac bit-predicate (class==10 & row<7 & nasal==0 & free==0) == 14 vowels -> {'OK' if bit_pred_ac == ac_14 else 'FAIL'}")

    expected_ik = [0x88, 0x90, 0x98, 0xA0]
    if [hex(c) for c in ik] != [hex(c) for c in expected_ik]:
        failures.append(f"ik mismatch vs HTML: {[hex(c) for c in ik]} != {[hex(c) for c in expected_ik]}")

    # width check: 64 codes 0x80-0xBF, occupied 28, free 36
    occupied = set(c for c, _, _, _, _ in table)
    assert occupied == {code(r, l, n) for r in range(7) for l in (0, 1) for n in (0, 1)}
    free_codes = [c for c in range(0x80, 0xC0) if c not in occupied]
    print(f"\noccupied={len(occupied)} (expect 28), free in 0x80-0xBF={len(free_codes)} (expect 36)")

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(" -", f)
        return 1
    print("\nALL CHECKS PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(main())