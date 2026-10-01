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

Nothing here is Sanskrit or Ukrainian: no layout, no sign, no spelling. Sound labels in
documents and tests are **IAST** (lowercase, with diacritics) and **Devanāgarī**; the earlier SLP1
labels and capital letters are being removed from the lab **by the owner's decision (2026-10-01)**;
identity is the code, never a label. Non-sounds (it-markers) are `meta` cells that name their
place on the sūtra path. Notation for the variant marks (anusvāra, visarga, avagraha, pluta,
nasalization) with sources: `docs/upc14-candidate-spec-2026-10-01.md` §6; plan for the oracle
files: `docs/upc14-oracles-iast-plan-2026-10-01.md`.

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
in a 128-byte table (its own Latin notation, SLP1; not ours); it does not define a code space.

## Consonant sandhi as graph queries (`upc14v2_sandhi.py`)

Every class a rule needs is **computed from the graph**, not listed: `jhal jaś jhaś khar car
yar ñam jhay aṭ` are intervals of the sūtra path; `ku cu ṭu tu pu` are savarṇa classes of a
varga. Every substitution is the same query, the nearest vertex of a target set. Rules
implemented: 8.2.39, 8.4.40, 8.4.41, 8.4.45, 8.4.53/55, 8.4.60, 8.4.62, 8.4.63 for a pada-final
stop meeting the next sound, and ṇatva (8.4.2) inside a word. A result carries the trace of
sūtras that fired (`t + ca` → 8.2.39 t→d, 8.4.40 d→j, 8.4.55 j→c). Rules apply once each in
ascending sūtra number; that order is one choice (see below).

**Evidence** (`test_upc14v2_sandhi.py`, 23 tests, local run):
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

**Contact in both directions (`contact`, added after the Kāśikā reading by the shiva agent).**
8.4.40 and 8.4.41 act whether the s/t-varga comes before *or after* the palatal/retroflex
(Kāśikā lines 83644-83721: yajñaḥ, yācñā, peṣṭā, kṛṣīṣṭhāḥ as well as vṛkṣaś śete, agnicid ḍīnaḥ).
The blocks come before the substitution: 8.4.42 (word-final ṭ-varga does not make a following
s/t-varga retroflex), 8.4.43 (t-varga before ṣ), **8.4.44 śāt (after ś a t-varga does not become
palatal: praśnaḥ, viśnaḥ)**. So 8.4.44 is implemented, as a block, and the Coq file that
encodes it as a positive palatalization departs from the Kāśikā. The old `final_stop` still
implements only the left-hand direction and is what the 97/99 vidyut comparison exercises.

**Found by the shiva agent's Kāśikā check of the consonant sandhi** (`docs/upc14v2-kasika-consonant-sandhi-2026-09-30.md`
on their branch) and fixed here: (1) a word-final `n` does not become ṇ (8.4.37: vṛkṣān, arīn,
girīn), `natva(..., complete_pada=True)` now skips it; (2) 8.4.60 `n + l` gives the **nasal l**
(bhavāṃl lunāti), not the oral one; (3) the docstring claimed "ascending sutra number", the code
runs 8.4.60 before 8.4.45 and 8.4.55, and 8.4.53 is not a separate step; now stated as it is.
Still open from that check: the vārttika "chatvam ami" of 8.4.63 (ś→ch before m, l is not
handled: tacchlokena, tacchmaśruṇā), the optional (vā) results as sets, "nitya" before a nasal
affix (vāṅmayam), 8.4.53/55 inside a word (bhettā), 8.4.38-39. The Kāśikā prints agnicitśete under
8.4.63 (t not changed to c), which contradicts 8.4.40 that the code applies; it looks like a
source error and is not resolved.

**Not implemented, on purpose:** 8.4.65, the optional (vā) alternatives of 8.4.45 and 8.4.62 as a
set, anusvāra and visarga, `n`-final insertions (`n + c → ṃś c`), `āṅ`/`num` in ṇatva, and the
exceptions of 8.4.42 (nām, navati, nagarī), which need morphology.

**Also surveyed:** `SandhiKosh` (LREC benchmark corpus in `.xls`; not parsed, no reader
installed), `shantanuo/sandhi` (GPL-3: read only, nothing copied), `eGangotri/indicTools`
(MIT, transliteration and sandhi tooling; not evaluated), `nileshshrivastava/Maheshwara`
(MIT, six documents, no code: a vision statement aligned with "derive, do not assume").

## Vowel sandhi as graph queries (`upc14v2_vowel_sandhi.py`)

6.1.101 (dīrgha), 6.1.88 (vṛddhi), 6.1.87 (guṇa; ṛ ḷ + `r l` by 1.1.51), 6.1.77 (yaṇ), 6.1.78
(ayavāyāv: decompose the join of places, yaṇ the second part), and the two apavādas
6.1.109 (word-final e/o + short a) and 6.1.97 (a inside a word + a/e/o; Kāśikā (lines 53311-53313, per the shiva agent, not re-read here) names only 6.1.101 as its apavāda target and adds that vṛddhi 6.1.88 would otherwise apply in pace, yaje: an inference that 6.1.97 also prevents it). A result carries
its sūtra trace and `ekadesa`: under the adhikāra 6.1.84 (valid up to and including 6.1.111,
Kāśikā on 6.1.84 as tabulated by the panini agent) the pair becomes one sound (87, 88, 97,
101, 109); 6.1.77 and 6.1.78 stand before it and replace one sound.

**Evidence** (`test_upc14v2_vowel_sandhi.py`, 16 tests; local run): **127 of 154** vowel+vowel
rows of vidyut's generated rules agree; the other **27 are exactly the optional elision of y
after a/ā**; the Kāśikā allows it for y AND v (8.3.19, line 80714: pada-final, after avarṇa, before aś, optional; per the shiva agent, not re-read here), vidyut applies it to y only (o/au rows keep v), this graph applies neither (each of
the 27 equals this graph's result with the `y` removed). The Kāśikā examples the panini agent
tabulated (dadhy atra, cayanam, lavanam, cāyakaḥ, lāvakaḥ, agne 'tra, vāyo 'tra) hold; cayanam and
lavanam hold only with `padanta=False`, the default `padanta=True` sends e/o + a to 6.1.109 (agne 'tra).
Not implemented: 6.1.94, the plutapūrva exception of 6.1.77, the avagraha sign, 8.3.19,
anything needing morphology. The plutapūrva exception needs no morphology (pluta is the length coordinate; it needs a 3-sound window `vowel_sandhi(prev, left, right)`); 6.1.94-95 need an upasarga+dhātu flag (Kāśikā lines 53224, 53263, per the shiva agent).

## it-saṃjñā on the path (`is_it`, `test_upc14v2_it.py`)

Kāśikā readings by the shiva agent (kAshikAvRRitti.txt; **(q)** quotation, **(i)** inference):
**(q)** 1.3.3 halantyam (line 3349): the final hal of a text unit is `it` (it names ṇ, k, ṅ, c; for the
sutra text "upadese ity eva"); **(q)** the Kāśikā itself resolves the circularity of `hal` inside
1.3.3 (line ~3358: a tantra use, so the `l` of hal is `it` too); **(q)** 1.1.71 (line 1647): the first
sound with the `it`-final one denotes the sounds fallen between them **and its own form**; **(q)**
1.3.9 tasya lopaḥ: the `it` disappears completely. **(i)** The other ten markers (ṭ ṇ m ñ ṣ ś v y r
l) are the same rule for the other sutras; the Kāśikā does not list them. 1.3.4–1.3.8 concern
affixes and roots, not the Śiva-sūtras.

In the graph a node is `it` exactly when it is the last token of its sutra, so 1.3.3 is read off
the structure (14 nodes, all consonants of `hal`); a marker is a `meta` cell that only names its
place (it is never a sound vertex, which is 1.3.9 in code); a pratyāhāra contains its first sound
(its own form) and the sounds between, never the marker. **Which occurrence of a repeated marker
(ṇ twice, h twice) 1.1.71 takes is not said in the Kāśikā**; the graph uses the tradition of
`ksetra/astadhyayi/occurrence-resolution.yaml` (aṇ first ṇ, iṇ second), which is an assumption
here. **Update (task #53, shiva agent, Kāśikā lines 99-103, 1622-1623, 43710):** the source **is** in the
Kāśikā, not in the sūtras themselves: `iṇ` always takes the later ṇ, while `aṇ` takes the earlier one
except for the single use named by 1.1.69 (`aṇudit savarṇasya cāpratyayaḥ`: `aṇ` with the later
ṇ); the yaml's "8.3.32" is a wrong number for 1.1.69 (8.3.32 is an example of the pratyāhāra `ṅam`). The
choice of occurrence is therefore fixed by the Kāśikā's list of uses, not derived from the sūtras. The
second `h`: the Kāśikā explains (lines 165-176) that the later `h` serves the hal-groups (ral 1.2.26,
śal 3.1.45, val, jhal) and the earlier `h` serves `aṭ` and `aś` (haśi ca 6.1.114). Status of those yaml
entries is now "located: Kāśikā, not the sūtras themselves".
Not checked: Kāśikā 1.3.10-1.3.12, and the Mahābhāṣya/Śikṣā view of the count of 14.

## Design assumptions and where they come from (independent review, shiva agent)

Recorded after an independent review that read the Kāśikā text in `ksetra/`
(`kAshikAvRRitti.txt`; line numbers are the reviewer's):

- **The aperture split (sibilant = 2, vowel = 3) is an assumption made to reproduce** "r and the
  sibilants have no savarṇa" (line 392), **not derived from the Kāśikā**. Line 386 names four
  ābhyantara efforts only (spṛṣṭa, īṣatspṛṣṭa, saṃvṛta, vivṛta); there ūṣman and vowels share
  `vivṛta` and are kept apart only by 1.1.10 (ac vs hal). `ai`/`au` as a fifth step (wide vowel) is
  also mine (from Śikṣā tradition, not the Kāśikā).
- **Short `a` is vivṛta.** Before the first sūtra the Kāśikā (lines 29-33) says the short `a`, closed
  in speech, is treated as vivṛta in the śāstra "for the sake of savarṇa" (`tasya prayogārtham a iti
  8.4.68`). That is a direct source for putting `a` on the vowel step of the aperture path; the
  sibilant/vowel split itself is still the assumption described above.
- **ḷ is nasal by pratijñā** (line 107: `lakāre tv anunāsikaḥ pratijñāyate`), and `r` in 1.1.51 is the
  pratyāhāra r+l; this supports `a + ḷ → al` (1.1.51) in `upc14v2_vowel_sandhi`.
- **ṛ and ḷ.** The Kāśikā records a stipulation making them savarṇa (lines 53198, 53396, a
  vārttika); 1.1.9 as written does not (their places differ). `savarna(..., vartika=True)`
  adds it; the default is the sūtra as written. vidyut's `savarna_str` includes it.
- **Voicing and aspiration of ś ṣ s h** (aghoṣa mahāprāṇa, and h ghoṣa mahāprāṇa) are Śikṣā /
  Siddhāntakaumudī tradition; the reviewer did not find them in the Kāśikā (searched for
  mahāprāṇa, alpaprāṇa, ghoṣa, aghoṣa). vidyut disagrees on the sibilants; the interval
  result holds under both (54/55/54). **`h` = throat** matches the tradition; not checked in the corpus.
- **8.4.44 śāt is a prohibition** (lines 83760-83769: after ś the t-varga does not undergo the
  preceding rule: praśnaḥ, viśnaḥ), and 8.4.43 toḥ ṣi is the same for ṣ (line 83746); the Coq
  file that encodes 8.4.44 as a positive palatalization departs from the Kāśikā. Both are now
  implemented as blocks in `contact`.
- **8.4.2** (lines 82823-82856): the intervening sounds are aṭ, ku, pu, āṅ, num (examples
  karaṇam, arkeṇa, darpeṇa, carmaṇā, paryāṇaddham, bṛṃhaṇam). ś ṣ s are not in aṭ, ku or pu,
  which is the reviewer's inference from the definition of the pratyāhāra; no Kāśikā line
  names them, so `kṛśānu` keeping `n` is derived, not quoted.
- **"r and the sibilants have no savarṇa"** is at line 392, and "vargīya only with vargīya of the
  same varga" at line 393. Both are quoted in `docs/savarna-model-validation-2026-08-30.md`.
- **`nearest` distance order.** The distance is lexicographic: place, then aperture, then voice,
  aspiration, nasal, length. Only "place first" is argued from 1.1.50; **the order after place is
  a choice**, not found in the Kāśikā. An exact tie raises `Ambiguous` and is never resolved.
- **`nearest` is ambiguous outside a rule's domain**, on purpose: for the yaṇ target set that is
  k kh g gh ṅ h a; for jaś/car it is v e o ai au. A test runs every rule over all 47×47 pairs of
  sounds (42 plus the five long vowels) and none reaches an `Ambiguous`. This found a real case:
  `v + nasal` under 8.4.45, where v has two places and no varga nasal is nearest; the rule now gives
  the semivowel its own nasal form (`v~`) instead.
- **e and ai are not savarṇa** with each other: this is an **inference** from Kāśikā line 390
  ("sandhyakṣarāṇāṃ hrasvā na santi, tāny api dvādaśaprabhedāni": e o ai au have twelve kinds
  each and no short forms), **not a quotation**; no line says "e is not savarṇa to ai". The
  default `savarna` gives 22 classes: five vargas, the singletons y r l v ś ṣ s h, and the vowel
  groups a, i, u, ṛ, ḷ, e, o, ai, au (50 pairs).
- **8.4.45 for the semivowels.** Kāśikā 8.4.45 (lines 83774-83787, read by the reviewer) has only
  stop examples (vāṅnayati, vāgnayati, agnicin nayati, ...). Line 391 says y v l have a nasal and
  a non-nasal form and **r has no nasal form**. So y v l become `y~ v~ l~` (an **inference from 391**,
  not an example of 8.4.45) and r is left alone.
- **ṛ and ḷ in 6.1.101** (lines 389, 6.1.101 and its vārttikas, tabulated by the reviewer): **ḷ has
  no long form** (`lṛvarṇasya dīrghā na santi`), so `dirgha(ḷ, ḷ)` raises. With `vartika=True` the
  pairs give the long ṛ or the vowel that follows (hotṝkāraḥ / hotṛkāraḥ; hotṝkāraḥ / hotlṛkāraḥ),
  as a set of variants (vā), no variant is primary (`sounds` holds one of them, `options` the others); ḷ+ḷ and ṛ+ḷ, ḷ+ṛ have no Kāśikā example (ḷ+ḷ and ḷ+ṛ follow by
  symmetry, an inference). Without the vartika, ṛ+ḷ, ḷ+ṛ, ḷ+ḷ fall to 6.1.77 and are marked
  `not attested` in `Result.note`.
- A pratyāhāra whose start sound is recited twice (h): the default takes the first recitation,
  as `occurrence-resolution.yaml` does for aṭ aś haś iṇ hal. `strict=True` raises
  `AmbiguousStart` instead of guessing, which is what case `later-h-is-not-initial-h-for-hR` (the fixture's own id; its `R` is ṇ) of
  the panini fixture asks; the fixture's five positive cases agree with the graph.

## Status and sources (folded 2026-10-02 from `docs/upc14-status-and-sources-2026-10-01.md`)

Status: **candidate**, not canon. All PRs of the stack (#60-#73) are in master; the text codec (IAST, Devanagari, Cyrillic, pluta), `pratyahara_named` (43 names), the three-valued `savarna_status`, the SLP1-free core and `e_voice` validation (#73) are part of the code described above. Every typed edge is one bit operation on the 14-bit code (`upc14v2_bitops.py`, `docs/upc14-bit-edge-laws-2026-10-02.md`: on the derivation instances; wider over all vertices).

### Джерела, знайдені після першої версії специфікації

- **Місце звуків** (r мурдха, l дантья, h горло): Siddhāntakaumudī і Laghukaumudī на 1.1.9 (`ashtadhyayi-data` ключ 11009); у Kāśikā txt переліку sthāna нема. **Голос/придих ś ṣ s h:** Laghukaumudī («हशः संवारा नादा घोषाश्च», «शलश्च महाप्राणाः», «खरो … अघोषाः»). Обидва раніше були «з пам'яті», тепер source-confirmed.
- **Aperture-розщеплення sibilant=2/vowel=3:** Laghukaumudī (п'ять ābhyantara-prayatna, ūṣman = īṣadvivṛta); Kāśikā і Siddhāntakaumudī мають чотири. **a = vowel:** Kāśikā txt 29-33 (a у шастрі vivṛta).
- **e~ai, o~au:** жодне джерело не визначає; Kāśikā за власним означенням зробила б їх savarṇa; у коді `savarna_status` = None (а `savarna` False як припущення ai/au п'ятий ступінь).
- **Класи голосних:** Kāśikā txt 387-390 (a i u ṛ: 18 видів, ḷ: 12 без довгого, e o ai au: 12 без короткого); довжина і назалізація в одному класі savarṇa.
- **Pluta:** корпус Kāśikā: ३ 6451 раз, ā3 43 проти a3 1; Деванагарі `भो३इ` = `bho3i` кодека.
- **Кирилиця:** книга власника «Бгаґавад-ґіта як вона є», «Як читати санскрит», сс. 810-812 (g = ґ, придих = стоп + г, ai = аі); ṅ ñ ṇ нерозбірливі на фото: hypothesis.

### Перевірки

| Перевірка | Результат | Хто |
|---|---|---|
| pratyāhāra як інтервал: оракул ashtadhyayi.com | 43/43 | тести, підтвердила «паніні» |
| pratyāhāra: усі комбінації (початок, маркер, nth) проти другої реалізації | 305/305 | «паніні» (з сутр, не з коду) |
| іменовані pratyāhāra | 43/43 (після виправлення `bhaś` → `bhaṣ`, додано `ṅam`) | «паніні», я |
| кількість pratyāhāra за маркерами проти вступу Kāśikā | 13 із 14 (cay) | я |
| savarṇa: 861 пара, з vārttika й без | 0 розбіжностей | «паніні» |
| варіанти (довгі/назалізовані/pluta): 44 звуки, 1892 порівняння | 0; 64 «не визначено» (e~ai, o~au) | «паніні» |
| кодек тексту (IAST, Деванагарі, кирилиця): round-trip, ін'єктивність, `transcode`, суворий декодер | 0 збоїв у моєму fuzz (випадкові послідовності довжини 4-14, 100 000 випадкових рядків на письмо, вичерпно довжини 1-2) і в тестах координатора (довжина 3 вичерпно) | я, координатор |
| типізовані ребра і Hamming: 36 з 861 пар на відстані 1; 12 з 39 типізованих ребер не Hamming-1 | вимір | я |

### Що лишається відкритим

1. e~ai/o~au (джерело мовчить); 2. знаки кирилиці ṅ ñ ṇ (потрібне чітке фото с. 811, видання книги); 3. назалізація в IAST/Деванагарі (U+0303, ँ): hypothesis (у корпусі Kāśikā немає жодного ँ); 4. anusvāra, visarga, avagraha: поза 42 звуками (див. `docs/upc14-open-decisions-2026-10-01.md`); 5. рішення власника про мерж PR і про критерії «candidate → canon»; 6. cay у вступі Kāśikā.

## Honest limits

- The feature assignment (place of each sound, aperture, which sounds are aspirated or
  voiced, `a` = lift of `g`, `h` = lift of `gh`) is a **modelling choice from the
  traditional classification**, checked for internal consistency only, not against a
  primary phonetic source. The pratyāhāra tests do not depend on it; the `nearest` and
  natural-class results do.
- The order of the sūtras is one canon; the interval result says nothing about why.
- Not covered: accent, optionality (`vā`), `chatvam ami`, `nitya` before a nasal affix, 8.4.53/55 inside a word (see docs/upc14v2-kasika-consonant-sandhi-2026-09-30.md; consonant sandhi itself now has 8.2.39, 8.4.40-45, 8.4.55, 8.4.60-63 and natva), `ṛ`+`a` = `ar` (a sequence, not a
  vertex), full Aṣṭādhyāyī ordering (rule conflict, 1.4.2), pluta usage, meta cells beyond
  markers, any text outside the 42 sounds.
- 14 bits leave most of 16384 codes unused; nothing is claimed about packing or hardware.
  "Two per FPGA cell" is arithmetic (2 × 14 = 28, fpga-lisp `README.md:15`).
- Tests and model are by one author; the YAML sources are separate.

## Non-claim

An engineering model. It is not evidence about how Pāṇini worked, and it does not modify
the transmitted Śiva-sūtra text.
