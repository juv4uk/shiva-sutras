# UPC-14 v2: a graph canon (experiment, shiva-sutras#44)

**Status: EXPERIMENTAL CANDIDATE, separate from v1 (PR #45) and from UPC-7.** No UPC-7 cell,
table, pin or witness is touched. Owner direction (2026-09-30): change the paradigm; UPC-7
is not the canon, UPC-14 will be; do not bind Sanskrit or Ukrainian yet; move from the
Śiva-sūtras toward the full Pāṇinian grammar; use graph theory, not a table.

## The paradigm shift

v1 numbered the sounds in the sūtra order and hung modifiers on the number. **v2 has no
row per sound.** A sound is a **vertex of a graph** and its 14-bit code is the vertex's
**coordinates**. The whole inventory is *derived from one seed* (`k`) by typed edges.

```text
code (14) = meta(1) | place(5) | nasal(1) | aperture(3) | length(2) | voice(1) | asp(1)
```

| field | graph | edges |
|---|---|---|
| place | Boolean lattice on 5 atoms K T M D O (throat, palate, roof, teeth, lips); join = OR | `shift` walks the spine K→T→M→D→O; `join` unions places |
| nasal | one atom, apart from place (1.1.8) | `nasal` |
| aperture | path P5: stop – semivowel – sibilant – vowel – wide vowel | `lift` raises it |
| length | path P3: short – long – pluta | `long` |
| voice, asp | one edge each | `voice`, `asp` |

`python3 prototype/upc14v2.py --dot` prints the derivation as a Graphviz digraph
(42 vertices, 41 typed edges: the varga rows by `asp`/`voice`/`nasal`, the next varga by
`shift`, semivowels/sibilants/h/vowels by `lift`, `e o` by `join`, `ai au` by `lift`).

**What is irreducible input:** the seed, the edge types, and the sūtra order itself.
Everything else (the 42 codes, savarṇa, pratyāhāra, guṇa, vṛddhi, yaṇ, jaś) is computed.

Nothing here is Sanskrit or Ukrainian: no layout, no sign, no spelling. SLP1 letters are
debug labels for the sūtra text and tests only. Non-sounds (it-markers) are `meta` cells
that name their place on the sūtra path.

## Grammar as graph queries

| rule | as a query |
|---|---|
| pratyāhāra | an interval of the sūtra path (a path over the vertices) |
| 1.1.9 savarṇa | equal place and aperture; the nose is a separate atom |
| 6.1.101 dīrgha | savarṇa simple vowels merge into the long one |
| 6.1.87 / 6.1.88 guṇa, vṛddhi | join of places; vṛddhi also lifts the aperture |
| 1.1.50 sthāne'ntaratamaḥ | the **nearest vertex** of a target set, place first; a tie raises `Ambiguous` |
| 6.1.77 yaṇ, 8.2.39 jaś | the same `nearest` query with different target sets |

## Evidence (empirically confirmed, local run; `test_upc14v2.py`, 29 tests)

**Non-trivial (these could have failed):**
- **39 of 42** classical pratyāhāras of `ksetra/astadhyayi/pratyahara-usage.yaml` equal an
  interval of the path (the other 3 entries of that YAML are wrong; see PR #45).
- `nearest` gives **i u ṛ ḷ → y v r l** (yaṇ) and **all 20 stops → the voiced unaspirated
  stop of the same varga** (jaś). No edge says so; place distance does. `u → v` works
  because `v` has teeth *and* lips and is nearer than `y`, `r`, `l`.
- The five vargas are **isomorphic**: `shift` commutes with `asp`, `voice`, `nasal`
  (a 5 × 5 grid graph = place spine × member row).
- **Natural classes.** Of 195 classes definable by ≤ 3 of the atoms above, **54 are
  intervals in the sūtra order**; 50 random orders (seed 14) never exceed 40 (200 orders in
  the exploration: mean 33, max 37). All five aperture classes, voiced, unvoiced, nasal and
  long are intervals; **no single place is**. The sūtras arrange the sounds by aperture and
  voice and leave place to the varga structure.
- Ill-formed codes (no articulator, off a path, a consonant with length, a meta cell)
  fail closed.

**Trivial by construction (do not count as evidence):** `guṇa` and `vṛddhi` reproduce
`e o ai au` because those are *defined* as joins of places. `e` has no unique nearest
`a`/`i` (correctly `Ambiguous`).

## Honest limits

- The feature assignment (place of each sound, aperture, which sounds are aspirated or
  voiced, `a` = lift of `g`, `h` = lift of `gh`) is a **modelling choice from the
  traditional classification**, checked for internal consistency only, not against a
  primary phonetic source. The pratyāhāra tests do not depend on it; the `nearest` and
  natural-class results do.
- The order of the sūtras is one canon; the interval result says nothing about why.
- Not covered: consonant sandhi beyond jaś, accent, `ṛ`+`a` = `ar` (a sequence, not a
  vertex), full Aṣṭādhyāyī ordering (rule conflict, 1.4.2), pluta usage, meta cells beyond
  markers, any text outside the 42 sounds.
- 14 bits leave most of 16384 codes unused; nothing is claimed about packing or hardware.
  "Two per FPGA cell" is arithmetic (2 × 14 = 28, fpga-lisp `README.md:15`).
- Tests and model are by one author; the YAML sources are separate.

## Non-claim

An engineering model. It is not evidence about how Pāṇini worked, and it does not modify
the transmitted Śiva-sūtra text.
