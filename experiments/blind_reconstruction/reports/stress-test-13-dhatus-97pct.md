# Stress Test: 13 dhātus × 3 forms — 97.4% recall

**Date**: 2026-09-07
**Status**: COMPLETED
**Score**: 38/39 (97.4%)
**Previous**: 24/27 (88.9%) on 9 dhātus, 4 classes

## Test matrix

| # | Dhātu | Class | 3sg (tip) | 3pl (jhi) | 1sg (mip) | Status |
|:---|:---|:---|:---|:---|:---|:---|
| 1 | bhU | 1 | bhavati ✓ | bhavanti ✓ | bhavAmi ✓ | 3/3 |
| 2 | nI | 1 | nayati ✓ | nayanti ✓ | nayAmi ✓ | 3/3 |
| 3 | stu | 1 | stavati ✓ | stavanti ✓ | stavAmi ✓ | 3/3 |
| 4 | ad | 2 | atti ✓ | adnti ✗ | admi ✓ | 2/3 |
| 5 | paz | 4 | pazyati ✓ | pazyanti ✓ | pazyAmi ✓ | 3/3 |
| 6 | dfz | 4 | dfzyati ✓ | dfzyanti ✓ | dfzyAmi ✓ | 3/3 |
| 7 | su | 5 | sunoti ✓ | sunvanti ✓ | sunomi ✓ | 3/3 |
| 8 | pac | 6 | pacati ✓ | pacanti ✓ | pacAmi ✓ | 3/3 |
| 9 | tud | 6 | tudati ✓ | tudanti ✓ | tudAmi ✓ | 3/3 |
| 10 | kfS | 6 | kfSati ✓ | kfSanti ✓ | kfSAmi ✓ | 3/3 |
| 11 | tan | 8 | tanoti ✓ | tanvanti ✓ | tanomi ✓ | 3/3 |
| 12 | cur | 10 | corayati ✓ | corayanti ✓ | corayAmi ✓ | 3/3 |
| 13 | kruS | 10 | kroSayati ✓ | kroSayanti ✓ | kroSayAmi ✓ | 3/3 |

## Classes tested

| Class | Vikaraṇa | ṭit | Dhātus tested | Score |
|:---|:---|:---|:---|:---|
| 1 (Śap) | a | Yes | bhU, nI, stu | 9/9 |
| 2 (none) | — | — | ad | 2/3 |
| 4 (Śya) | sya | No | paz, dfz | 6/6 |
| 5 (Śnu) | nu | Yes | su | 3/3 |
| 6 (Śa) | a | No | pac, tud, kfS | 9/9 |
| 8 (u) | u | Yes | tan | 3/3 |
| 10 (Ṇic) | i+Śap | Yes | cur, kruS | 6/6 |
| **Total** | | | **13** | **38/39** |

## Remaining failure

**ad (class 2) 3pl**: ad + nti → adnti. Expected "atti".
- Class 2 has no vikaraṇa (adhātuka)
- d before n: 8.4.55 (jhalāṃ jhaśi) requires n to be khar (voiceless)
- n IS khar → d should become t → atnti → atti?
- But our 8.4.55 only checks immediate next sound, not across morpheme boundaries
- Also: dt → tt assimilation (8.4.40: stoḥ ścunā ścuḥ?)

## Derivation pipeline (all classes)

```
dhātu + vikaraṇa + tiṅ
  → it-lopa (1.3.3-9: remove it-markers from vikaraṇa and tiṅ)
  → jhi→nti ādeśa (8.4.62)
  → ṭere (3.4.79: ātmanepada only)
  → vṛddhi (7.3.89: 1st person, ṭit only → a→A)
  → guṇa/yaṇ:
      Class 1:   guṇa on dhātu vowel (7.3.84)
      Class 5,8: guṇa on vikaraṇa vowel for 3sg/1sg (7.3.84)
                 yaṇ on vikaraṇa vowel for 3pl (6.4.87)
      Class 10:  guṇa on ALL vowels (7.2.115 + 7.3.84)
  → eco (6.1.78: e/o + vowel → ay/av)
  → 8.4.55 (jhalāṃ jhaśi: voiced → voiceless before voiceless)
  → surface form
```

## History

| Date | Score | Dhātus | Classes | Change |
|:---|:---|:---|:---|:---|
| 2026-09-06 | 14/27 (52%) | 9 | 4 | Initial expanded test |
| 2026-09-06 | 24/27 (89%) | 9 | 4 | Fixed vṛddhi, guṇa, vikaraṇa, encoding |
| 2026-09-07 | 38/39 (97%) | 13 | 7 | Added classes 5, 8; guṇa/yaṇ split |

## Sources

- Aṣṭādhyāyī (Baums, GRETIL): 3.1.68-81, 6.4.87, 7.3.84, 7.2.115
- Kāśikā (Sharma ed., GRETIL): on 3.1.73, 6.4.87
