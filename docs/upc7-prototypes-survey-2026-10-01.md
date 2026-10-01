# The 7-bit prototypes: a survey (research, hypothesis)

Coordinator survey, 2026-10-01, read-only: no prototype was changed. The measuring script is `prototype/survey_7bit.py`; its output is the table below (empirical, local run on the branch of PR #65, not CI).

## 1. What exists

| id | prototype | where | what it is | tests (local) |
|---|---|---|---|---|
| H | hand-placed UPC-7 (geometry v2) | `upc7_geometry.py`, `upc7_layouts.py`, `upc7_table.py`, `upc7-table.tsv` | 2-bit class + 5-bit payload, cells placed by hand; layouts `sa-slp1`, `sa-iast`, `sa-deva`, `uk`, `bits`; the table SENS pins as Text7 | 8 + 53 OK |
| L | legacy UPC-7 | `upc7.py` | the low half of the flat UPC-8 table (code = position in the sutra order); a donor witness | 7 OK |
| V | varṇa7 | `varna7-prana14/varna7.py` | 4 regions (sparśa, antastha-ūṣman, svara, saṃjñā), the same shape as H with other names | 1 script, "all tests passed" |
| A | akṣara7 | `akshara7.py` | 1 family bit + 6-bit payload; code = index in a fixed order of the 42 sounds; 14 marker cells | 7 OK |
| T | tantu7 | `graph7.py` | code = vertex index (0..41) in the same order as A; the graph (edges) is derived, not stored in the code | 7 OK |
| D | **saṅkṣepa7** (संक्षेप, "abridgment"): UPC-7 derived from the UPC-14 graph | `upc7_derive.py` (PR #65) | a cell computed from the UPC-14 vertex by rule | 8 OK |
| — | witnesses and audit | `upc7_cold_witness.lisp`, `upc7_cold_verify.c`, `upc7_corpus_audit.py`, `upc7-corpus-report.json` | pin the table; audit a corpus (evidence only, it cannot assign identities) | audit run, not the witnesses |
| — | SENS side | `sens/crates/sens/src/text7.rs`, `text7_projection*.rs`, `contracts/text7-upc7.lock` | `Text7` = an exact sequence of 7-bit cells (one per `u8`, high bit forbidden); projections generated from the pinned table | not run |

The SENS lock pins `prototype/upc7-table.tsv` (sha256 `dbceb273…`) and `prototype/upc7_layouts.py` (sha256 `f225761d…`) at shiva-sutras revision `062b2685…`. **A change to either file (moving r, l, h; removing the `sa-slp1` layout) needs a new lock and regenerated projections on the SENS side.**

## 2. Measured

On the 42 sounds, same measures for every prototype (`python3 prototype/survey_7bit.py`):

| | 42 sounds placed | distinct cells | pratyāhāras contiguous in code order (of 43) | savarṇa read from the bits: mismatches with the graph (of 1764 ordered pairs) |
|---|---|---|---|---|
| H hand table | 42 | 42 | 0 | 6 |
| D derived | 42 | 42 | 0 | 4 |
| V varṇa7 | 42 | 42 | 0 | 4 |
| A akṣara7 | 42 | 42 | 25 | not computable from bits (a code is an index) |
| T tantu7 | 42 | 42 | 25 | not computable from bits |
| L legacy | 42 | 42 | 39 | not computable from bits |

Cells equal between prototypes (of 42): D–V 41, H–V 40, H–D 39; A–T 42; A–L and T–L 22; H or D or V against A, T, L: 1.

## 3. What it shows

1. **Two families, not six.** H, D and V are one geometry: class from the effort, payload = place × member (stops), macro-place × slot (the rest), row × nose × length (vowels). A, T and L are ordinals: the code is an index.
2. **A and T have the same 42 codes** (42 of 42 equal). They differ in what they add (A: 14 marker cells; T: a derived edge list, nothing in the code).
3. **Structure in the bits is what lets savarṇa be a rule.** Only H, D, V have it. For D and V the 4 mismatches are exactly e~ai, o~au (both orders), the two pairs that the sources do not decide (the UPC-14 `savarna_status` returns `None` for them). H has 2 more: **r~l**, because H puts r and l in the same dental place with the same effort. That is a defect of the hand table: r is mūrdhanya and l is dantya, so they are not savarṇa.
4. **The sutra order is what makes a pratyāhāra an interval of codes.** L (code = position in the sutra order) has it for 39 of 43; the 4 exceptions are exactly the ones that contain the repeated h (`val`, `ral`, `jhal`, `śal`). A and T lose it (25 of 43) because their order departs from the sutra order after ñ m ṅ ṇ n (j jh b bh g gh k kh …). H, D, V have none (0 of 43): their geometry serves savarṇa, not intervals.
5. **Where r, l, h are placed.** H puts r with s l (dental), h glottal and voiceless. The sources (Siddhāntakaumudī and Laghukaumudī on 1.1.9, read by the shiva and panini agents; the Kāśikā at 1.1.9 does not list the places) say: h kaṇṭhya (and haś, śal ∋ h: ghoṣa, mahāprāṇa), ṛ ṭu r ṣ mūrdhanya, ḷ tu l s dantya. D and V follow the sources; they differ from each other only in the slot of l (D: sonorant, V: its own lateral slot; the lateral slot is not supported by the sources).
6. **Coverage.** A, T, L: the 42 sounds only (A also 14 markers). H and V: also ā ī ū ṝ (and V ḹ, which does not exist, Kāśikā txt 389), nasal-vowel cells, anusvāra, visarga, signs. V's README says its saṃjñā region holds the it-markers; its `SAMJNA_NAMES` holds ASCII signs only (found by the panini agent), so V cannot name the 14 markers.
7. **V is H's geometry with the three places corrected.** 40 of 42 cells equal H's; the shape (4 regions, `place*5+member`, `row<<2|nose<<1|length`, 32 signs) is the same. The authorship question is the one already raised for PRĀṆA-14 vs UPC-14 v2 (92 of 250 lines equal); it is not decided here.

## 4. Options (not decisions)

- **Keep H.** Nothing changes on the SENS side. Known: r~l false positive in a bit rule; r, l, h placed against the sources.
- **Move to D** (generate the geometry from UPC-14): changes 3 cells (r, l, h), fixes the r~l pair, removes the hand placement. Requires a new SENS lock and regenerated projections; the slot of l is a decision.
- **Add an interval layer** (a code order = the sutra order) next to the geometry: would make pratyāhāra an interval for 39 of 43 (not 43: the repeated h). Not built.

## 5. Not checked

CI; the cold witnesses (`upc7_cold_witness.lisp`, `upc7_cold_verify.c`) and the SENS `Text7` code were not run; the Ukrainian extension cells and signs were not measured; the corpus audit was only read (its `sa-slp1` fixture reads `siva-sutras-encoded.yaml`, which keeps SLP1); the claim that D and V "follow the sources" for r, l, h rests on the Siddhāntakaumudī / Laghukaumudī lines read by two other agents, not re-read here.
