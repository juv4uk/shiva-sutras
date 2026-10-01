# The logic of the sound domain: every typed edge is one bit operation (research, hypothesis)

Written 2026-10-02 after reading how SENS states the logic of its domains D3 (bīja3) and D4. Not a SENS domain, not ratified;
it is the sound/text counterpart, in their style: *generation first, placement last; laws that can fail; negative results kept.*

## 1. What SENS does for D3 and D4 (read, not re-derived)

- D3 `bīja3`: 8 roots in 3 bits; the only proven generator is CAR/CDR: `101 CAR`, `110 CDR`, and appending a bit composes (`...0` CAR, `...1` CDR).
- D4: each D3 prefix gets a lane (`000x` meta, `001x` abstraction, `010x` predicate refinement, `011x` traversal, `100x` construction, `101x` CAR, `110x` CDR,
  `111x` environment); the low bit has a polarity law (`0` = current/focus, `1` = continuation/expansion); only the selector lanes have a proven prefix
  theorem, the rest are placement hypotheses; two cells are **left empty** (`0101`, `1001`) instead of inventing functions.
- Their discipline: a prefix edge gets meaning only through executable typed evidence; `word boundary != prefix lineage != semantic derivation`.

## 2. The sound domain, in the same terms

UPC-14 v2 derives the 42 sounds from one seed `k` by typed edges. The new observation, checked exhaustively (`prototype/upc14v2_bitops.py`,
`test_upc14v2_bitops.py`): **every typed edge is one machine operation on the 14-bit code.**

| edge | meaning | bit form on the code | law |
|---|---|---|---|
| asp | stop <-> its aspirate | `c ^ 0x0001` | involution, a constant flip of bit 0 |
| voice | voiceless <-> voiced | `c ^ 0x0002` | involution, a constant flip of bit 1 |
| nasal | the stop's nasal | `(c | 0x0080 | 0x0002) & ~1` | partial, one-way (idempotent), not an involution |
| shift | next place on the spine | place field `<< 1` (bits 8..12) | partial successor, fails at the end |
| lift n | aperture `+ n` | `c + 16n` | partial successor on a path of 5 |
| join | union of places | `c | atoms << 8` | boolean OR |
| long | length `+ 1` | `c + 4` below plutā, the identity at plutā (saturates) | partial successor on a path of 3 |

**Checked:** on all 2232 vertices (of 16384 codes) the graph edge `upc14v2.e_*` and the bit form give the same result (or both raise); the edges are **partial** (e.g. asp is defined on 248 of the 2232 vertices, shift on 1080), so "one bit operation" is a statement about the vertices where the edge is defined, and `long` saturates at plutā (an independent check by the panini agent found the 496 vertices where a plain `+4` would differ); asp, voice and nasal are
**one constant xor mask each** over every instance in the derivation (10, 5, 5 pairs); asp and voice commute and are involutions on every stop.

This is the sound-domain counterpart of "appending a bit is a composition step": the **suffix-bit law** `x0 = unaspirated, x1 = aspirated`, and `0x = unvoiced, 1x = voiced` one bit up.

## 3. Negative results (first-class)

1. **The 7-bit prototypes have no such law.** The same asp pairs give 4 different xor masks in the hand-placed UPC-7 table (and 4 in akshara7); voice gives 3 and 4.
   Reason for the hand table: `payload = place * 5 + member` is not bit-aligned (a carry), chosen to fit 25 stops in 5 bits. The derived saṅkṣepa7 has the same shape. A bit-aligned
   stop word needs `place * 8 + member` = 40 cells, i.e. more than the 32 of a class.
2. **Hamming-1 does not cover the edges** (hypothesis-level, the shiva agent measured it independently): in the 14-bit code asp, voice and nasal are 1 bit apart, but shift is 2, join 2, lift 1..3. (Measured by the shiva agent on the derivation instances: asp 1 [10 pairs], voice 1 [5], nasal 1 [5], shift 2 [4], join 2 [4], lift 1..3. Over ALL 2232 vertices the distances are wider: shift 2 or 4, nasal 0..3 (0 on an already nasal vertex), join 0..1, lift1 1..3. The statement holds for the derivation, not for every vertex.)
   "Typed edge = one bit operation" is true; "typed edge = one bit changed" is false.
3. **Place is not binary.** The place field is a boolean lattice of 5 atoms (join = OR) and a spine (shift = `<< 1`), not a binary choice; the five places are not a prefix tree.
4. **A defect found by the check:** `upc14v2.e_voice` is `c ^ 2` without validating its input: it accepts all 14152 non-vertex codes, the only one of the nine edges that does
   (pinned in `test_known_defect_…`). A fail-closed fix is one line (`unpack(c)`). **Fixed afterwards** in `upc14v2.e_voice` (the test now expects no edge to accept a non-vertex).

## 4. What this does and does not claim

- It does not say UPC-14 *is* a SENS domain, nor propose sound words inside the bīja3/D4 space. It states a law the sound code has and the 7-bit prototypes lack; that is evidence for
  the canon question (UPC-14 vs UPC-7), not a decision.
- Generation first: the **irreducible input** is the seed `k`, the 7 edge types and the order of the sūtras; every other code is derived. Cells that are valid vertices but are not
  one of the 42 sounds, the long and nasal vowel forms, or `y~ v~ l~` are **not admitted**; the text codec fails closed on them (it does not invent a sound to fill a cell).
- Not checked: a benchmark of "derive by bit operations" against table lookup; behaviour for the plutā length; the Ukrainian extension; CI.

## 5. Коротко українською

Кожне типізоване ребро графа звуків UPC-14 це **одна машинна операція над 14-бітним кодом**: придих це `xor` біта 0, дзвінкість `xor` біта 1, носовість встановлення біта 7, зсув місця
це `<< 1` поля місця, підняття апертури це `+16n`, об'єднення місць це OR, довгота `+4`. Перевірено вичерпно на всіх 2232 вершинах: графове ребро й бітова форма однакові. У жодному з 7-бітних
прототипів цього закону нема (різні маски `xor`), бо `place*5+member` не вирівняне по бітах. Знайдено дефект: `e_voice` не перевіряє вхід (приймає 14152 не-вершини), виправлення одним рядком у ядрі
(зона шіви). Це свідчення в питанні «що канон», не рішення.
