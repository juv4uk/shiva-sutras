# UPC-8 Pratyāhāra Authority Implementation Plan

> **For agentic workers:** this plan records the implemented first slice. Future extensions must keep the same authority boundary: canon first, derived UPC view second.

**Goal:** Compare canon-derived pratyāhāra member sets with explicit UPC feature predicates without creating a second semantic authority.

**Architecture:** Reuse `prototype/upc8_pratyahara_probe/probe.py`, which already reads `ksetra/canon/siva-sutras.yaml`. Canonical membership comes only from `build_pratyaharas()`. UPC membership is independently derived from `SA_FEATURES` and then classified as `EXACT`, `PARTIAL`, or `NOT_SINGLE_PREDICATE`.

**Spec:** `docs/superpowers/specs/2026-09-18-upc8-pratyahara-authority-design.md`

## Global constraints

- `ksetra/canon/siva-sutras.yaml` is immutable authority and is not edited.
- `sounds` and `it_marker_iast` remain distinct.
- Pratyāhāra keys are the probe's literal `start sound + it-marker` form (`ñm`, `jś`, `hl`), not normalized display spellings such as `ñam`/`jaś`.
- Generated predicates/masks are derived engineering views, never canonical definitions.
- Current `SA_FEATURES` has no aspiration dimension; no test may pretend otherwise.
- No hard-coded pratyāhāra membership table is added.

---

### Task 1: RED comparison API

**Files:**
- Create: `prototype/upc8_pratyahara_probe/test_compare.py`
- Modify: `prototype/upc8_pratyahara_probe/probe.py`

- [x] Add a test importing `compare_pratyahara_to_upc()` before the API exists.
- [x] Verify RED: focused pytest fails at import because the API is missing.
- [x] Correct the initial test notation after discovering the existing probe keys are `ñm`/`jś`, not `ñam`/`jaś`.

### Task 2: First EXACT and negative witness

- [x] Add `nasal` predicate over existing `SA_FEATURES` (`manner == 3`).
- [x] Derive canonical membership from the immutable YAML through existing probe functions.
- [x] Verify `ñm ↔ nasal` is `EXACT` with `ñ m ṅ ṇ n`.
- [x] Represent `voiced-unaspirated-stop` as unavailable in the current feature space rather than fabricating an aspiration distinction.
- [x] Verify `jś ↔ voiced-unaspirated-stop` is `NOT_SINGLE_PREDICATE` with an explicit reason.

### Task 3: Whole-consonant witness and duplicate canonical position

- [x] Add RED test for `hl ↔ consonant`.
- [x] Verify RED fails because `consonant` predicate does not yet exist.
- [x] Add `consonant` predicate (`manner != 5`).
- [x] Normalize repeated canonical sound positions to unique set members while preserving first-occurrence order.
- [x] Verify `hl` produces 33 unique consonants and repeated `h` appears once.

### Task 4: Documentation

- [x] Document the canonical-vs-derived boundary in `prototype/upc8_pratyahara_probe/README.md`.
- [x] Record positive witnesses (`ñm`, `hl`) and negative witness (`jś`).
- [x] State explicitly that `EXACT` is an engineering equality of sets, not a historical claim that Pāṇini used binary encoding.

### Task 5: Verification / coordination

- [x] Focused command: `python -m pytest prototype/upc8_pratyahara_probe/test_compare.py -q` → `3 passed` in the isolated local replica.
- [x] Syntax command: `python -m py_compile prototype/upc8_pratyahara_probe/probe.py prototype/upc8_pratyahara_probe/test_compare.py` → exit 0.
- [x] GitHub compare confirms no canon file changed; production diff adds only comparison code to the existing probe.
- [x] Draft PR #8 records the RED/GREEN evidence and coordination constraints.
- [ ] Repository-wide automated CI remains unavailable in this repository; do not claim a full-suite CI result.

## Next slice (not part of this PR)

Do not add more hand-maintained Python tables. The next useful experiment is to add an occurrence-aware canonical-selector result for ambiguous repeated it-markers, then decide whether the stabilized comparison result should be emitted as a machine-readable artifact for Lisp/C/RTL consumers.