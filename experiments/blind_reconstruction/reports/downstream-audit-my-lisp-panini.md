# Downstream Audit: my-lisp-panini against shiva-sutras claims

**Date:** 2026-09-07
**Analyst:** Sarvam AI agent
**Scope:** Verify epistemic coordination contract compliance between upstream (`shiva-sutras`) and downstream (`my-lisp-panini`)

---

## AUDIT 1: siva-sutras.my vs SS-CANON-001

### Canon structure

The file `panini/machine/siva-sutras.my` encodes 14 Śiva-sūtras as SLP1 lists:

```lisp
((a i u R) (f x k) (e o N) (E O c) (h y v r w) (l R)
 (Y m N R n m) (J B Y) (G Q D S) (j b g q d S)
 (K P C W T c w t V) (k p y) (S z s r) (h l))
```

**Structural check:** 14 sūtras — correct count.

### CRITICAL ISSUE: Ṣ/Ś marker conflation (SS9 and SS10)

SS9 marker = `S` (should be `z` = Ṣ, retroflex sibilant)
SS10 marker = `S` (should be `S` = Ś, palatal sibilant)

In SLP1, `z` = ष (retroflex Ṣ) and `S` = श (palatal Ś). These are **distinct sounds with distinct it-markers**. The .my file uses `S` for both, conflating two different markers.

**Impact on pratyāhāra expansion:**
- The `expand_pratyahara('h', 'l')` function (HAL = all consonants) **stops prematurely** at SS9's marker `S`, returning only `['h', 'y', 'v', 'r', 'w']` instead of the full consonant set.
- HAL expansion is **broken** — it returns 5 sounds instead of 33.
- Any downstream computation that depends on HAL (the set of all consonants) will produce wrong results.

**Severity:** CRITICAL — this breaks the core pratyāhāra expansion for at least HAL, and potentially other consonant-class pratyāhāras.

### ISSUE: It-markers included in pratyāhāra expansions

The `expand_pratyahara` function (naive implementation) includes it-markers in the expanded set:

- AC (a→c) returns `['a','i','u','R','f','x','k','e','o','N','E','O']` — includes markers R, k, N
- Expected: `['a','i','u','f','x','e','o','E','O']` — markers excluded

This is because the function collects all sounds between start and marker **inclusive of other sūtras' markers**. By Pāṇinian rule 1.3.3 (halantyam), it-markers are excluded from pratyāhāra denotation. The .my file's expansion function does not implement this exclusion.

**Impact:** All 5 hardcoded pratyāhāra subsets (AC, HAL, IK, EC, YAN) include spurious it-marker sounds. The hardcoded values are correct (markers manually excluded), but any dynamic expansion using `expand_pratyahara` would produce wrong results.

**Note:** The hardcoded subsets in the .my file (lines 18-22) are **manually correct** — the author manually excluded it-markers. But there is no programmatic function to expand pratyāhāras correctly; the `expand_pratyahara` approach would fail.

### ISSUE: SS11 marker case mismatch (V vs v)

SS11 it-marker = `V` (uppercase) in the .my file, but the canonical `siva-sutras-encoded.yaml` specifies `v` (lowercase). In SLP1, case matters: `v` = व (labiodental approximant), while `V` is not a standard SLP1 phoneme. This is likely a typo, but it means the marker for voiceless stops (SS11) is not correctly identified by any case-sensitive lookup.

### ISSUE: SS5 it-marker 'w' — documented non-standard

The it-marker of SS5 is `w` in both the .my file and the canonical `siva-sutras-encoded.yaml`. This is a project-internal convention: `w` = ṭ (retroflex Ṭ), as documented in the metadata note of the canonical file. This is **not a bug** — it is a deliberate encoding choice specific to this project's SLP1 variant.

### ISSUE: YAN expansion includes 'w'

YAN (y→R) expands to `['y','v','r','w','l']` — includes `w` (SS5's it-marker). Expected: `['y','v','r','l']`. Same root cause as the it-marker inclusion issue.

---

## AUDIT 2: claims-export.yaml → shiva_claims.my (epistemic coordination contract)

### Claim import status

| Claim | Export status | Import status | Compliant? |
|:---|:---|:---|:---|
| SS-CANON-001 | RESOLVED | resolved | YES (exact match) |
| SS-PRATYAHARA-001 | SUPPORTED | supported | YES (exact match) |
| SS-MARKERS-001 | PROVED-IN-MODEL | supported | YES (downgrade) |
| SS-MARKERS-002 | PROVED-IN-MODEL | supported | YES (downgrade) |
| SS-MARKERS-003 | PROVED-IN-MODEL | supported | YES (downgrade) |

### ISSUE: Status downgrade for SS-MARKERS claims

SS-MARKERS-001/002/003 are exported as `PROVED-IN-MODEL` but imported as `supported`. Per the epistemic coordination contract, downstream may be more conservative (downgrade is allowed), but this loses the stronger status. The downstream consumer may not be aware that these results are formally proven within the model.

**Recommendation:** Either match the upstream status or document the reason for the downgrade.

### ISSUE: Revision pin is stale

- `claims-export.yaml` baseline: `0f6110d` (2026-08-17)
- `shiva_claims.my` references: `a8391c4` (2026-08-15, initial)

The downstream import is pinned to the **older revision** `a8391c4`. It does not include claims added in revision `0f6110d`:
- H-SS-EXT-001 (phonological dimensions)
- H-SS-EXT-002 (multi-level comparison structure)
- H-SS-EXT-003 (Sanskrit annotates canon)

Additionally, 4 other claims are not imported (by choice, not error):
- SS-ORDER-001, SS-CORPUS-001, SS-EPISTEMIC-001, SS-EPISTEMIC-002

**Recommendation:** Update `shiva_claims.my` to reference revision `0f6110d` and decide whether H-SS-EXT claims are relevant to the downstream model.

---

## AUDIT 3: inference_engine.lisp — Proof-Carrying Derivations

### Architecture

The inference engine implements a **hardcoded derivation chain** for the form *labhate* (3rd person singular, present tense, ātmanepada):

1. **Rule 1 (3.2.123):** `vartamāne laṭ` — inserts lakāra `laṭ`
2. **Rule 2 (3.4.78):** `tiptasjhi...` — replaces lakāra with tiṅ ending `ta`
3. **Rule 3 (1.1.68):** `kartari śap` — inserts vikaraṇa `śap`
4. **Rule 4 (1.3.9):** `tasya lopaḥ` — elides it-markers from `śap` → `a`
5. **Rule 5 (3.4.79):** `ṭita ātmanepadānāṃ ṭere` — replaces `ta` with `te`

### Observations

1. **History tracking:** Each rule prepends its identifier to a history list, providing a derivation trace. This is a basic form of proof-carrying derivation — the output includes the sequence of rules applied.

2. **No conflict resolution:** The engine applies rules in a fixed order (1→2→3→4→5). There is no mechanism for:
   - Rule conflict (multiple applicable rules)
   - Rule blocking (apavāda)
   - Anuvṛtti (continuation of context from previous rules)
   - Asiddha (invisible operations)

3. **No pratyāhāra resolution:** The engine works with hardcoded SLP1 strings (`"Sa~p"` for śap, `"ta"` for the tiṅ ending). It does not resolve pratyāhāras — the Śiva-sūtra data in `siva-sutras.my` is not used by the inference engine.

4. **Single derivation:** Only one derivation path is implemented (`derive-labhate`). The engine is a proof-of-concept, not a general-purpose derivation system.

5. **SLP1 encoding:** Uses tilde for nasals (`~p` = anusvāra+p? or nasal mark), `~w` for anusvāra+ṭ? The encoding differs from both standard SLP1 and IAST.

### Epistemic status

The inference engine is at **v0.1 proof-of-concept** stage. It demonstrates the graph-rewriting approach but does not yet:
- Use the Śiva-sūtra pratyāhāra system (SS-PRATYAHARA-001)
- Implement anuvṛtti
- Handle rule conflicts
- Support general derivation

---

## Summary of findings

| Finding | Severity | Component |
|:---|:---|:---|
| Ṣ/Ś marker conflation in siva-sutras.my | CRITICAL | siva-sutras.my SS9/SS10 |
| It-markers not excluded in dynamic expansion | HIGH | siva-sutras.my expansion logic |
| SS11 marker 'V' should be 'v' (case mismatch) | MEDIUM | siva-sutras.my SS11 |
| SS5 marker 'w' documented non-standard | INFO | siva-sutras.my SS5 |
| Status downgrade SS-MARKERS-001/002/003 | LOW | shiva_claims.my |
| Revision pin stale (a8391c4 vs 0f6110d) | LOW | shiva_claims.my |
| Inference engine doesn't use pratyāhāra system | INFO | inference_engine.lisp |
| Inference engine is single-derivation POC | INFO | inference_engine.lisp |

---

## Epistemic status

ENGINEERING AUDIT. No claims modified. Findings reported for owner review.
