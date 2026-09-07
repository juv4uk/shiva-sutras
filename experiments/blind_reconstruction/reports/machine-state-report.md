# Machine State Report: my-lisp-panini computational coherence

**Date:** 2026-09-07 (updated)
**Report type:** Computational coherence evidence (downstream → upstream)
**Source repo:** `juv4uk/my-lisp-panini` (commit `5c759be`)
**Target repo:** `juv4uk/shiva-sutras`
**Epistemic layer:** ENGINEERING (machine-level observation, not historical claim)

---

## 1. Purpose

L-001 (outcome A) established that the canonical sound-class system is textually recoverable from the Aṣṭādhyāyī. This report documents whether those classes are *computationally coherent* — i.e., whether a machine that uses them as its core data structure can produce correct Sanskrit verbal forms.

This is not proof of historical intent. It is evidence that the formal system "works" end-to-end.

## 2. Machine architecture

The machine consists of 10 modules in a layered pipeline:

```
CANON (Śiva-sūtras, 14 sūtras, 42 sounds)
    ↓ resolve-pratyahara (ādir antyena sahetā, 1.1.71)
siva-sutras.my (resolver: adi + marker → sound set)
    ↓ in-ac?, in-hal?, in-ik?, in-jhash?, in-khar?, ...
phonology.my (canon-derived predicates + SLP1 validator)
    ↓ apply-sandhi(final, next)
sandhi.my (4 rules: 6.1.77, 8.3.23, 8.4.55, 8.4.58)
    ↓
ting.my (18 tiṅ endings + ALL 10 vikaraṇa classes + it-lopa + ṭere)
    ↓
derivation.my (pipeline: it-lopa → ṭere → vṛddhi → guṇa/yaṇ → eco → 8.4.55)
    ↓
trace.my (falsifiable sūtra-cited step traces)
    ↓
paradigm.my (9 × parasmaipada + 9 × ātmanepada forms)
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

### 3.2 Verbal derivation — 13 dhātus × 3 forms (38/39 = 97.4%)

| Dhātu | Class | 3sg (tip) | 3pl (jhi) | 1sg (mip) | Score |
|:---|:---|:---|:---|:---|:---|
| bhU | 1 (Śap) | bhavati ✓ | bhavanti ✓ | bhavAmi ✓ | 3/3 |
| nI | 1 (Śap) | nayati ✓ | nayanti ✓ | nayAmi ✓ | 3/3 |
| stu | 1 (Śap) | stavati ✓ | stavanti ✓ | stavAmi ✓ | 3/3 |
| ad | 2 (none) | atti ✓ | adnti ✗ | admi ✓ | 2/3 |
| paz | 4 (Śya) | pazyati ✓ | pazyanti ✓ | pazyAmi ✓ | 3/3 |
| dfz | 4 (Śya) | dfzyati ✓ | dfzyanti ✓ | dfzyAmi ✓ | 3/3 |
| su | 5 (Śnu) | sunoti ✓ | sunvanti ✓ | sunomi ✓ | 3/3 |
| pac | 6 (Śa) | pacati ✓ | pacanti ✓ | pacAmi ✓ | 3/3 |
| tud | 6 (Śa) | tudati ✓ | tudanti ✓ | tudAmi ✓ | 3/3 |
| kfS | 6 (Śa) | kfSati ✓ | kfSanti ✓ | kfSAmi ✓ | 3/3 |
| tan | 8 (u) | tanoti ✓ | tanvanti ✓ | tanomi ✓ | 3/3 |
| cur | 10 (Ṇic) | corayati ✓ | corayanti ✓ | corayAmi ✓ | 3/3 |
| kruS | 10 (Ṇic) | kroSayati ✓ | kroSayanti ✓ | kroSayAmi ✓ | 3/3 |

**Total: 38/39 (97.4%)**

### 3.3 Derivation pipeline

```
dhātu + vikaraṇa + tiṅ
  → it-lopa (1.3.3-9: remove it-markers from vikaraṇa and tiṅ)
  → jhi→nti ādeśa (8.4.62)
  → ṭere (3.4.79: ātmanepada only)
  → vṛddhi (7.3.101: 1st person, ṭit → a→ā)
  → guṇa/yaṇ:
      Class 1:   guṇa on dhātu vowel (7.3.84)
      Class 5,8: guṇa on vikaraṇa vowel for 3sg/1sg (7.3.84)
                 yaṇ on vikaraṇa vowel for 3pl (6.4.87) + a-insertion
      Class 10:  guṇa on ALL vowels (7.2.115 + 7.3.84)
  → eco (6.1.78: e/o + vowel → ay/av)
  → 8.4.55 (jhalāṃ jhaśi: voiced → voiceless before voiceless)
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

## 4. Score history

| Date | Score | Dhātus | Classes | Change |
|:---|:---|:---|:---|:---|
| 2026-09-06 | 14/27 (52%) | 9 | 4 | Initial expanded test |
| 2026-09-06 | 24/27 (89%) | 9 | 4 | Fixed vṛddhi, guṇa, vikaraṇa, SLP1 |
| 2026-09-07 | 38/39 (97%) | 13 | 7 | Added classes 5, 8; guṇa/yaṇ split |

## 5. Remaining failure

**ad (class 2) 3pl**: ad + nti → adnti. Expected: "atti".
- Class 2 has no vikaraṇa (adhātuka)
- Requires assimilation rule (8.4.40: stoḥ ścunā ścuḥ or similar)
- Known edge case, deferred

## 6. Journal references

- Journal 0017: Ṇic→aya resolved (guṇa-on-aṅga)
- Journal 0018: Unified guṇa-on-aṅga (classes 1, 5, 8, 10)
- Journal 0019: Hostile review relevance analysis
- Journal 0020: Classes 5, 8 working — 97.4%
- Journal 0021: Operation types, lakāra design, Siddhāntakaumudī reference

## 7. Sources

- Aṣṭādhyāyī (Baums, GRETIL): 3.1.68-81, 6.4.87, 7.3.84, 7.2.115, 8.4.55
- Kāśikā (Sharma ed., GRETIL): on 3.1.73, 6.4.87, 7.3.84
