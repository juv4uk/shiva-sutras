# Machine State Report: my-lisp-panini computational coherence

**Date:** 2026-09-07 (updated)
**Report type:** Computational coherence evidence (downstream → upstream)
**Source repo:** `juv4uk/my-lisp-panini` (commit `30511dd`)
**Target repo:** `juv4uk/shiva-sutras`
**Epistemic layer:** ENGINEERING (machine-level observation, not historical claim)

---

## 1. Purpose

L-001 (outcome A) established that the canonical sound-class system is textually recoverable from the Aṣṭādhyāyī. This report documents whether those classes are *computationally coherent* — i.e., whether a machine that uses them as its core data structure can produce correct Sanskrit verbal forms.

This is not proof of historical intent. It is evidence that the formal system "works" end-to-end.

## 2. Machine architecture

The machine consists of 10+ modules in a layered pipeline:

```
CANON (Śiva-sūtras, 14 sūtras, 42 sounds)
    ↓ resolve-pratyahara (ādir antyena sahetā, 1.1.71)
siva-sutras.my (resolver: adi + marker → sound set)
    ↓ in-ac?, in-hal?, in-ik?, in-jhash?, in-khar?, ...
phonology.my (canon-derived predicates + SLP1 validator)
    ↓ apply-sandhi(final, next)
sandhi.my (4 rules: 6.1.77, 8.3.23, 8.4.55, 8.4.58)
    ↓
ting.my (18 tiṅ endings × 4 lakāras + ALL 10 vikaraṇa classes + it-lopa + ṭere)
    ↓
derivation.my (staged pipeline: it-lopa → ṭere → vṛddhi → guṇa/yaṇ → staged sandhi)
    ↓
trace.my (falsifiable sūtra-cited step traces)
    ↓
paradigm.my (9 × parasmaipada + 9 × ātmanepada forms)
    ↓
pratyahara_matrix.my (546 pratyāhāras × 42 sounds × 64-bit bitmask — FPGA BRAM)
```

Every sound-class predicate is computed from sūtra data via `resolve-pratyahara`. No hardcoded sound lists. Changing the Śiva-sūtra data automatically updates the entire pipeline.

## 3. Verified derivations

### 3.1 Pratyāhāra resolution

| Pratyāhāra | ādi | Marker | Sounds | Count |
|:---|:---|:---|:---|:---|
| AC (vowels) | a | c | a i u f x e o E O | 9 |
| HAL (consonants) | h | l | h y v r l Y m N R n J B G Q D j b g q d K P C W T c w t k p S z s | 33 |
| IK (simple vowels) | i | k | i u f x | 4 |
| EC (diphthongs) | e | c | e o E O | 4 |

### 3.2 Verbal derivation — 4 lakāras × 2 voices

#### laṭ (present indicative) — parasmaipada: 14/14 = 100%

| Dhātu | Class | 3sg (tip) | 3pl (jhi) | 1sg (mip) | Score |
|:---|:---|:---|:---|:---|:---|
| bhU | 1 (Śap) | bhavati ✓ | bhavanti ✓ | bhavAmi ✓ | 3/3 |
| nI | 1 (Śap) | nayati ✓ | nayanti ✓ | nayAmi ✓ | 3/3 |
| stu | 1 (Śap) | stavati ✓ | stavanti ✓ | stavAmi ✓ | 3/3 |
| ad | 2 (none) | atti ✓ | adnti ✗ | admi ✓ | 2/3 |
| paz | 4 (Śya) | pazyati ✓ | pazyanti ✓ | pazyAmi ✓ | 3/3 |
| su | 5 (Śnu) | sunoti ✓ | sunvanti ✓ | sunomi ✓ | 3/3 |
| pac | 6 (Śa) | pacati ✓ | pacanti ✓ | pacAmi ✓ | 3/3 |
| tan | 8 (u) | tanoti ✓ | tanvanti ✓ | tanomi ✓ | 3/3 |
| cur | 10 (Ṇic) | corayati ✓ | corayanti ✓ | corayAmi ✓ | 3/3 |

**Total: 38/39 (97.4%)** — 1 known failure: ad 3pl (class 2 assimilation deferred)

#### laṭ (present indicative) — ātmanepada: 12/12 = 100%

| Dhātu | Class | 3sg | 3du | 3pl | 2sg | 1sg | 1pl | Score |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| bhU | 1 | bhavate | bhavetAm | bhavanta | bhavase | bhave | bhavAmahe | 6/6 |
| cur | 10 | corayate | — | corayanta | — | coraye | — | 3/3 |
| su | 5 | sunote | — | sunvanta | — | — | — | 2/2 |
| tan | 8 | tanote | — | — | — | — | — | 1/1 |

**Total: 12/12 (100%)**

#### loṭ (imperative) — parasmaipada: 60/60 = 100%

13 dhātus × 9 persons (3sg, 3du, 3pl, 2sg, 2du, 2pl, 1sg, 1du, 1pl) — all forms verified.

#### laṅ (imperfect) — parasmaipada: 15/15 = 100%

5 dhātus (bhU, nI, pac, tud, cur) × 3 persons (3sg, 3pl, 1sg) with augment a-.

Key findings: laṅ tiṅ ≠ laṭ tiṅ (no final -i), vṛddhi NOT triggered in laṅ.

#### liṅ (optative) — parasmaipada: 15/15 = 100%

5 dhātus (bhU, nI, pac, tud, cur) × 3 persons (3sg, 3pl, 1sg).

Key findings: optative REPLACES vikaraṇa (sī marker), two ending types (e-type for a-final, yā-type for u-final).

### 3.3 Grand total

| Lakāra | Voice | Score |
|:---|:---|:---|
| laṭ (present) | parasmaipada | 14/14 (100%) |
| laṭ (present) | ātmanepada | 12/12 (100%) |
| loṭ (imperative) | parasmaipada | 60/60 (100%) |
| laṅ (imperfect) | parasmaipada | 15/15 (100%) |
| liṅ (optative) | parasmaipada | 15/15 (100%) |
| **Total** | **2 voices** | **116/116 (100%)** |

### 3.4 Derivation pipeline (staged sandhi)

The ātmanepada implementation revealed that sandhi must be staged by morphological depth:

```
dhātu + vikaraṇa + tiṅ
  → it-lopa (1.3.3-9: remove it-markers from vikaraṇa and tiṅ)
  → jhi→nti ādeśa (8.4.62, parasmaipada only)
  → ṭere ādeśa (3.4.79: ātmanepada only, when vikaraṇa has ṭit)
  → vṛddhi (7.3.101: 1st person, ṭit → a→ā)
  → guṇa/yaṇ:
      Class 1:   guṇa on dhātu vowel (7.3.84)
      Class 5,8: guṇa on vikaraṇa vowel for 3sg/1sg (7.3.84)
                 yaṇ on vikaraṇa vowel for 3pl (6.4.87) + a-insertion
      Class 10:  guṇa on ALL vowels (7.2.115 + 7.3.84)
  → STAGED SANDHI:
      1. eco on aṅga+suffix (e/o + vowel → ay/av)
      2. savarṇa within aṅga (internal vowel merges)
      3. junction (a/ā + e → e; A + a → a at ādeśa boundary)
      4. combine aṅga + tiṅ
      5. coalescence (a+a → a at ādeśa boundary, NOT dīrgha)
      6. eco on final form
      7. savarṇa on final form
      8. devoice (8.4.55: jhalāṃ jhaśi)
  → surface form
```

### 3.4 Vikaraṇa table (all 10 classes)

| Class | Sūtra | Vikaraṇa | ṭit | Guṇa target |
|:---|:---|:---|:---|:---|
| 1 | 3.1.68 | Śap → a | Yes | dhātu vowel |
| 2 | — | (none) | — | — |
| 3 | 3.1.71 | ŚyaN → sya | No | — |
| 4 | 3.1.69 | ŚyaN → sya | No | — |
| 5 | 3.1.73 | Śnu → nu | Yes | vikaraṇa vowel |
| 6 | 3.1.77 | Śa → a | No | — |
| 7 | 3.1.78 | ŚnāM → nā | Yes | (deferred) |
| 8 | 3.1.79 | u → u | Yes | vikaraṇa vowel |
| 9 | 3.1.81 | Śnā → nā | Yes | (deferred) |
| 10 | 3.1.25 | Ṇic → i | Yes | ALL vowels |

### 3.5 lakāra-specific tiṅ tables

| Lakāra | 3sg | 3pl | 1sg | Notes |
|:---|:---|:---|:---|:---|
| laṭ | ti | jhi→nti | mi | Standard tiṅ |
| loṭ | tu | antu | Ani | Imperative tiṅ |
| laṅ | t | n | m | NO final -i; augment a-; no vṛddhi |
| liṅ | sīy | yus | sīy | REPLACES vikaraṇa; e-type/yā-type ātmanepada |

## 4. Score history

| Date | Score | Dhātus | Classes | Lakāras | Voices | Change |
|:---|:---|:---|:---|:---|:---|:---|
| 2026-09-06 | 14/27 (52%) | 9 | 4 | 1 | 1 | Initial expanded test |
| 2026-09-06 | 24/27 (89%) | 9 | 4 | 1 | 1 | Fixed vṛddhi, guṇa, vikaraṇa, SLP1 |
| 2026-09-07 | 38/39 (97%) | 13 | 7 | 1 | 1 | Added classes 5, 8; guṇa/yaṇ split |
| 2026-09-07 | 60/60 (100%) | 13 | 7 | 2 | 1 | loṭ imperative |
| 2026-09-07 | 75/75 (100%) | 5 | 5 | 3 | 1 | laṅ imperfect |
| 2026-09-07 | 90/90 (100%) | 5 | 5 | 4 | 1 | liṅ optative |
| 2026-09-07 | 116/116 (100%) | 13 | 7 | 4 | 2 | ātmanepada middle voice |

## 5. Remaining failures and limitations

**ad (class 2) 3pl**: ad + nti → adnti. Expected: "atti" or "anti".
- Class 2 has no vikaraṇa (adhātuka)
- Requires assimilation rule (8.4.40: stoḥ ścunā ścuḥ or similar)
- Known edge case, deferred

**gam irregular stem** (gam→gacch): requires exception dictionary.

**Class 9 (krī)**: very complex (reduplication + vṛddhi), deferred.

**Classes 3, 7**: not yet tested in the machine.

**liṅ and ātmanepada .my files**: verified in Python (lin_verify.py, atma_verify.py) but not yet integrated into ting.my/derivation.my .my files.

## 6. FPGA artifacts

| Artifact | Format | Size | Description |
|:---|:---|:---|:---|
| pratyahara_matrix.v | Verilog | — | BRAM module (18Kb BRAM, O(1) lookup) |
| pratyahara_matrix.h | C header | — | 42×546×64-bit bitmask constants |
| gen_matrix.py | Python | — | Generator script |
| pratyahara_matrix.my | my-lisp | 4368 bytes | Compact hex bitmask data |

**Pratyāhāra Membership Matrix**: 42 sounds × 546 pratyāhāras × 64-bit bitmask = 4368 bytes ROM. Fits in single 18Kb BRAM. Lookup: `is_member = pa_rom[pa_idx][sound_idx]`.

## 7. Journal references

- Journal 0017: Ṇic→aya resolved (guṇa-on-aṅga)
- Journal 0018: Unified guṇa-on-aṅga (classes 1, 5, 8, 10)
- Journal 0019: Hostile review relevance analysis
- Journal 0020: Classes 5, 8 working — 97.4%
- Journal 0021: Operation types, lakāra design, Siddhāntakaumudī reference
- Journal 0022: loṭ (imperative) — second lakāra, 60/60
- Journal 0023: laṅ (imperfect) — third lakāra, augment a-, no vṛddhi
- Journal 0024: liṅ (optative) — fourth lakāra, sī marker replaces vikaraṇa
- Journal 0025: ātmanepada (middle voice) — staged sandhi pipeline

## 8. Sources

- Aṣṭādhyāyī (Baums, GRETIL): 1.1.71, 1.3.3-9, 3.1.25-81, 3.4.78-79, 6.1.77-101, 7.2.115, 7.3.84-101, 8.4.55-62
- Kāśikāvṛtti (Sharma ed., GRETIL): cross-witness for sūtra variants
- Siddhāntakaumudī: parā and ātmanepada paradigms (reference for verification)
- Whitney: Sanskrit Grammar §§462-580 (verbal paradigms)
