# UPC-8 / Pratyāhāra Lisp Migration Plan

> **For agentic workers:** active repo-owned tooling moves from Python to my-lisp per issue #3. Keep Python only as a temporary parity witness until the Lisp path reproduces the same contract.

**Goal:** Replace the newly-added Python comparison direction with a native my-lisp regression slice and backport the corrected Lisp pratyāhāra masks.

**Authority:** `ksetra/canon/siva-sutras.yaml` remains immutable canon. `prototype_phonetics.lisp` is a derived engineering representation.

## Task 1 — Remove accidental new Python surface

- Revert `prototype/upc8_pratyahara_probe/probe.py` to `master`.
- Revert `prototype/upc8_pratyahara_probe/README.md` to `master`.
- Delete `prototype/upc8_pratyahara_probe/test_compare.py`.
- Verify branch diff has no new Python logic.

## Task 2 — Backport corrected Lisp masks

Source reference:
`juv4uk/my-lisp:prototype/lisp_core_phonetics/prototype_phonetics.lisp`

Expected corrected values:

```text
ac  = #x00000000000001FF
hal = #x000007FFFFFFFE00
al  = #x000007FFFFFFFFFF
ik  = #x000000000000001E
ec  = #x00000000000001E0
yar = #x000003FFFFFFFC00
Sar = #x000003800000000000
JaS = #x000000001F00000000
Jal = #x000003FFFF000200
```

Update only the derived Lisp knowledge-base copy; do not edit canon YAML.

## Task 3 — Native Lisp RED/GREEN regression

Create:
`prototype/lisp_core_phonetics/test_pratyahara_masks.lisp`

The script must:

1. read `prototype_phonetics.lisp` with `read-file` + `read`;
2. resolve `pratyahara-masks` and nested `mask` fields using `assoc`;
3. compare all nine corrected masks;
4. invoke an intentionally unbound failure symbol on mismatch;
5. print `pratyahara-mask-regression-green` on success.

Run with my-lisp-cli, for example:

```bash
cargo run -p my-lisp-cli -- ../shiva-sutras/prototype/lisp_core_phonetics/test_pratyahara_masks.lisp
```

Do not claim GREEN until the command has actually executed successfully.

## Task 4 — Next migration slice: `probe.py`

After this PR is green, migrate `prototype/upc8_pratyahara_probe/probe.py` separately:

1. capture deterministic Python fixtures/output;
2. write Lisp RED fixture consumer;
3. implement canon/pratyāhāra path in Lisp without changing research semantics;
4. differential parity Python ↔ Lisp;
5. switch documentation/automation to Lisp;
6. delete Python only after parity is green.

This keeps language migration separate from phonological-model changes.
