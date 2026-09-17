# UPC-8 Pratyāhāra Authority Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one executable comparison layer that derives canonical pratyāhāra members from the immutable Śiva-sūtra canon and compares them with explicit UPC feature predicates without creating a second semantic authority.

**Architecture:** Reuse `prototype/upc8_pratyahara_probe/probe.py` for canonical expansion and its existing curated Sanskrit feature registry. Add a small comparison API in the same prototype so the first slice has no duplicate canon parser or duplicate sound table. The comparison returns a typed status plus canonical/UPC member sets; no generated mask becomes authoritative.

**Tech Stack:** Python 3, existing PyYAML dependency, unittest/pytest-compatible test functions, existing `ksetra/canon/siva-sutras.yaml` authority.

**Spec:** `docs/superpowers/specs/2026-09-18-upc8-pratyahara-authority-design.md`

## Global Constraints

- `ksetra/canon/siva-sutras.yaml` is immutable authority and must not be edited.
- `sounds` and `it_marker_iast` remain distinct; markers never acquire UPC sound codes merely because spellings collide.
- Pratyāhāra names remain case-sensitive.
- UPC predicates are engineering interpretations, never replacements for canonical expansion.
- First slice covers only predicates whose feature semantics are already represented by `SA_FEATURES`; no new phonological ontology is invented.
- New code must not introduce another hard-coded pratyāhāra membership table.

---

### Task 1: RED comparison contract

**Files:**
- Create: `prototype/upc8_pratyahara_probe/test_compare.py`
- Modify later: `prototype/upc8_pratyahara_probe/probe.py`

**Interfaces:**
- Consumes: `load_sutras()`, `flat_sequence()`, `build_pratyaharas()`, `SA_FEATURES`.
- Produces expectation for `compare_pratyahara_to_upc(name: str, predicate: str) -> dict` with keys `status`, `canonical`, `upc`, `canonical_only`, `upc_only`.

- [ ] **Step 1: Write the failing test**

```python
from probe import compare_pratyahara_to_upc


def test_jas_matches_voiced_unaspirated_stops_exactly():
    result = compare_pratyahara_to_upc("jaś", "voiced-unaspirated-stop")
    assert result["status"] == "EXACT"
    assert result["canonical"] == ["j", "b", "g", "ḍ", "d"]
    assert result["upc"] == ["j", "b", "g", "ḍ", "d"]
    assert result["canonical_only"] == []
    assert result["upc_only"] == []
```

- [ ] **Step 2: Run test to verify RED**

Run: `python -m pytest prototype/upc8_pratyahara_probe/test_compare.py -q`
Expected: import/attribute failure because `compare_pratyahara_to_upc` does not exist yet.

- [ ] **Step 3: Commit RED witness**

Commit message: `test(upc8): require canonical-vs-feature pratyahara comparison`

### Task 2: GREEN minimal comparison

**Files:**
- Modify: `prototype/upc8_pratyahara_probe/probe.py`
- Test: `prototype/upc8_pratyahara_probe/test_compare.py`

**Interfaces:**
- Add `UPC_PREDICATES`, mapping predicate names to pure `SA_FEATURES` selectors.
- Add `compare_pratyahara_to_upc(name, predicate)` returning ordered lists in canonical sound order.

- [ ] **Step 1: Add the minimal predicate**

```python
UPC_PREDICATES = {
    "voiced-unaspirated-stop": lambda f: f[1] == 0 and f[2] == 1,
}
```

`SA_FEATURES` currently does not encode aspiration, so the first predicate must restrict itself to sounds that are represented as plain voiced stops in the existing registry. Do not claim that this proves an aspiration bit yet.

- [ ] **Step 2: Implement ordered set comparison**

Build canonical members from `build_pratyaharas`; derive UPC members by filtering `SA_FEATURES`; order both by canonical sequence; return `EXACT` only when sets are equal.

- [ ] **Step 3: Run focused test**

Run: `python -m pytest prototype/upc8_pratyahara_probe/test_compare.py -q`
Expected: PASS.

- [ ] **Step 4: Run existing probe tests / available Python regression suite**

Run the repository's existing Python test command if documented; at minimum run `python -m pytest prototype -q` when dependencies permit.

- [ ] **Step 5: Commit GREEN**

Commit message: `feat(upc8): compare canonical pratyahara with feature predicates`

### Task 3: Add mismatch classification without inventing semantics

**Files:**
- Modify: `prototype/upc8_pratyahara_probe/test_compare.py`
- Modify: `prototype/upc8_pratyahara_probe/probe.py`

**Interfaces:**
- `status`: `EXACT`, `PARTIAL`, or `NOT_SINGLE_PREDICATE` for implemented selectors. `AMBIGUOUS_CANONICAL_SELECTOR` is reserved for a later selector-aware canonical API and is not fabricated in this slice.

- [ ] **Step 1: Add a RED test for a deliberately broader predicate**

Use one known canonical class and a broader already-defined feature selector; assert `PARTIAL` and non-empty difference fields.

- [ ] **Step 2: Run RED, implement only the status classification, run GREEN**

Do not add new sound features solely to make the test convenient.

- [ ] **Step 3: Commit**

Commit message: `test(upc8): classify pratyahara predicate mismatches`

### Task 4: Document the experiment boundary

**Files:**
- Modify: `prototype/upc8_pratyahara_probe/README.md`

**Interfaces:**
- Document canonical source, comparison statuses, and the explicit non-claim that a matching predicate proves historical identity between Pāṇinian categories and binary encoding.

- [ ] **Step 1: Add a short section `Canonical set ↔ UPC predicate`**
- [ ] **Step 2: State that generated masks/predicates are derived engineering views**
- [ ] **Step 3: Record exact commands and observed test results**
- [ ] **Step 4: Commit**

Commit message: `docs(upc8): document pratyahara predicate experiment`

### Task 5: Integration gate

**Files:** none unless a discovered existing CI entry point requires registration.

- [ ] **Step 1: Run focused tests**
- [ ] **Step 2: Run broader repository tests available in CI**
- [ ] **Step 3: Inspect branch diff to verify canon files are untouched**
- [ ] **Step 4: Open/update PR with evidence and explicit limitations**
