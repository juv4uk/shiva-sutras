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

## Reference implementations surveyed (added after cloning them locally)

Owner suggestion: look at how others encoded Pāṇini. Cloned read-only (no fork needed to
read): `ambuda-org/vidyut` (Rust, MIT per its `Cargo.toml`, commit `8da2f90b`, 3 MB),
`ashtadhyayi-com/data` (no license declared; 1.7 GB, so 6 directories sparse-cloned, commit
`5744762f`), `kmadathil/sanskrit_parser` (MIT; surveyed, not used).

**Results** (`test_upc14v2_oracles.py`, 9 tests, all pass, local run):
- **43 of 43** phonetic pratyāhāras of ashtadhyayi.com equal an interval of the path. The two
  `aṇ` entries are the first and the second `ṇ`; `iṇ` uses the second. This also confirms
  that the three bad entries in `ksetra/.../pratyahara-usage.yaml` (`yaṇ`, `has`, `jhas`) are
  errors there: ashtadhyayi.com gives `yaṇ = {y v r l}`.
- vidyut's own unit-test vectors, copied as data with attribution: 8 pratyāhāras (`ac ec iṇ
  iṇ2 yaṇ hal ñam śar`), the savarṇa rows, and **all 24 pairs of `map(jhal → jaś)` and all 6 of
  `map(ku~ h → cu~)`**, which this graph's `nearest` reproduces (including `ś→j, ṣ→ḍ, s→d,
  h→g` and `h→jh`).
- **Robustness:** vidyut classifies the sibilants as unaspirated and with the semivowels, and
  `h` with the vowels; this graph puts them on one aperture step and aspirated. Re-running the
  natural-class experiment with vidyut's assignment gives **54 / 55 / 54** intervals (mine,
  sibilants unaspirated, vidyut-like), all above the ≤ 40 of random orders. The result is not
  an artifact of one school's feature choices.

**What vidyut shows** (source-confirmed, `vidyut-prakriya/src/sounds.rs`): it has the same
three ingredients in a different form. A per-sound record (`sthāna` list, `ghoṣa`, `prāṇa`,
`prayatna`), a `pratyahara()` that scans the sūtra list (`R2` = the second ṇ, our `nth=2`),
and a `map()` that picks the nearest sound by a **summed** distance that its own comment says
is **not symmetric** (a TODO). Here the distance is lexicographic, place first, symmetric, and
an exact tie raises `Ambiguous` instead of picking one. Vidyut's *identity* is a Latin letter
in a 128-byte table (SLP1); it does not define a code space.

## Consonant sandhi as graph queries (`upc14v2_sandhi.py`)

Every class a rule needs is **computed from the graph**, not listed: `jhal jaś jhaś khar car
yar ñam jhay aṭ` are intervals of the sūtra path; `ku cu ṭu tu pu` are savarṇa classes of a
varga. Every substitution is the same query, the nearest vertex of a target set. Rules
implemented: 8.2.39, 8.4.40, 8.4.41, 8.4.45, 8.4.53/55, 8.4.60, 8.4.62, 8.4.63 for a pada-final
stop meeting the next sound, and ṇatva (8.4.2) inside a word. A result carries the trace of
sūtras that fired (`t + ca` → 8.2.39 t→d, 8.4.40 d→j, 8.4.55 j→c). Rules apply once each in
ascending sūtra number; that order is one choice (see below).

**Evidence** (`test_upc14v2_sandhi.py`, 15 tests, local run):
- vs **vidyut's generated sandhi rules** (99 rows for a final k, ṭ, t, p, obtained by running
  `create_sandhi_rules` at commit `8da2f90b`): **97 of 99 agree**. The 2 that differ (`t+ñ`,
  `t+ṇ`) are a rule-order choice: ascending sūtra order gives `ñ ñ` (8.4.40 then 8.4.45),
  vidyut gives `n ñ`.
- vs the Coq formalization **paninian-verified** (`CharlesCNorton`, MIT; definitions parsed as
  written, Coq not run): palatalization, retroflexion and devoicing maps equal the nearest
  vertex (22 pairs).
- **Where the Coq file departs from the sūtra, and this graph does not:**
  (a) `voiced_of` maps kh → gh; 8.4.53 says jhal → jaś and jaś = j b g ḍ d has **no aspirate**,
  so the sūtra (and vidyut, and the nearest vertex) give kh → g. Exactly the five aspirates
  differ. (b) its ṇatva blocker list names palatals, retroflexes, dentals and `l` but not the
  sibilants, so `kṛśānu` would become `kṛśāṇu`; Pāṇini's own set (aṭ, ku, pu) excludes ś, and
  the graph-computed set keeps `n` (source-confirmed by reading; the Coq was not executed).
- The ṇatva word list (rāmeṇa, varṇa, purāṇa, brāhmaṇa; arjuna, arthana, kṛśānu unchanged) is
  standard spelling from my own knowledge, not an oracle; the Coq file's 4 examples are.

**Not implemented, on purpose:** 8.4.44 śāt (the Coq file encodes it as a positive
palatalization; I could not confirm that reading, so I do not claim it), 8.4.65, the optional
(vā) alternatives of 8.4.45 and 8.4.62 as a set, anusvāra and visarga, `n`-final insertions
(`n + c → ṃś c`), and `āṅ`/`num` in ṇatva.

**Also surveyed:** `SandhiKosh` (LREC benchmark corpus in `.xls`; not parsed, no reader
installed), `shantanuo/sandhi` (GPL-3: read only, nothing copied), `eGangotri/indicTools`
(MIT, transliteration and sandhi tooling; not evaluated), `nileshshrivastava/Maheshwara`
(MIT, six documents, no code: a vision statement aligned with "derive, do not assume").

## Vowel sandhi as graph queries (`upc14v2_vowel_sandhi.py`)

6.1.101 (dīrgha), 6.1.88 (vṛddhi), 6.1.87 (guṇa; ṛ ḷ + `r l` by 1.1.51), 6.1.77 (yaṇ), 6.1.78
(ayavāyāv: decompose the join of places, yaṇ the second part), and the two apavādas
6.1.109 (word-final e/o + short a) and 6.1.97 (a inside a word + a/e/o). A result carries
its sūtra trace and `ekadesa`: under the adhikāra 6.1.84 (valid up to and including 6.1.111,
Kāśikā on 6.1.84 as tabulated by the panini agent) the pair becomes one sound (87, 88, 97,
101, 109); 6.1.77 and 6.1.78 stand before it and replace one sound.

**Evidence** (`test_upc14v2_vowel_sandhi.py`, 16 tests; local run): **127 of 154** vowel+vowel
rows of vidyut's generated rules agree; the other **27 are exactly the optional elision of y
after a/ā (8.3.19)**, which vidyut applies to `e` and `ai` rows and this graph does not (each of
the 27 equals this graph's result with the `y` removed). The Kāśikā examples the panini agent
tabulated (dadhy atra, cayanam, lavanam, cāyakaḥ, lāvakaḥ, agne 'tra, vāyo 'tra) hold.
Not implemented: 6.1.94, the plutapūrva exception of 6.1.77, the avagraha sign, 8.3.19,
anything needing morphology.

## Design assumptions and where they come from (independent review, shiva agent)

Recorded after an independent review that read the Kāśikā text in `ksetra/`
(`kAshikAvRRitti.txt`; line numbers are the reviewer's):

- **The aperture split (sibilant = 2, vowel = 3) is an assumption made to reproduce** "r and the
  sibilants have no savarṇa" (line 392), **not derived from the Kāśikā**. Line 386 names four
  ābhyantara efforts only (spṛṣṭa, īṣatspṛṣṭa, saṃvṛta, vivṛta); there ūṣman and vowels share
  `vivṛta` and are kept apart only by 1.1.10 (ac vs hal). `ai`/`au` as a fifth step (wide vowel) is
  also mine (from Śikṣā tradition, not the Kāśikā).
- **ṛ and ḷ.** The Kāśikā records a stipulation making them savarṇa (lines 53198, 53396, a
  vārttika); 1.1.9 as written does not (their places differ). `savarna(..., vartika=True)`
  adds it; the default is the sūtra as written. vidyut's `savarna_str` includes it.
- **Voicing and aspiration of ś ṣ s h** (aghoṣa mahāprāṇa, and h ghoṣa mahāprāṇa) are Śikṣā /
  Siddhāntakaumudī tradition; the reviewer did not find them in the Kāśikā (searched for
  mahāprāṇa, alpaprāṇa, ghoṣa, aghoṣa). vidyut disagrees on the sibilants; the interval
  result holds under both (54/55/54). **`h` = throat** matches the tradition; not checked in the corpus.
- **8.4.44 śāt is a prohibition** (lines 83760-83769: after ś the t-varga does not undergo the
  preceding rule: praśnaḥ, viśnaḥ), and 8.4.43 toḥ ṣi is the same for ṣ (line 83746). So not
  implementing it was right, and the Coq file that encodes it as a positive palatalization
  departs from the Kāśikā.
- **8.4.2** (lines 82823-82856): the intervening sounds are aṭ, ku, pu, āṅ, num (examples
  karaṇam, arkeṇa, darpeṇa, carmaṇā, paryāṇaddham, bṛṃhaṇam). ś ṣ s are not in aṭ, ku or pu,
  which is the reviewer's inference from the definition of the pratyāhāra; no Kāśikā line
  names them, so `kṛśānu` keeping `n` is derived, not quoted.
- **"r and the sibilants have no savarṇa"** is at line 392, and "vargīya only with vargīya of the
  same varga" at line 393. Both are quoted in `docs/savarna-model-validation-2026-08-30.md`.
- A pratyāhāra whose start sound is recited twice (h): the default takes the first recitation,
  as `occurrence-resolution.yaml` does for aṭ aś haś iṇ hal. `strict=True` raises
  `AmbiguousStart` instead of guessing, which is what case `later-h-is-not-initial-h-for-hR` of
  the panini fixture asks; the fixture's five positive cases agree with the graph.

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
