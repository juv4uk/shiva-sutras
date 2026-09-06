# L-001 v5: Superset Validation — Compound/Sandhi-Form Breakthrough

**Date:** 2026-09-07
**Analyst:** Sarvam AI agent

## What changed from v4

v4 hypothesized 5 "virtual" pratyāhāras (uK, NaM, caY, Jaz, baS) that appeared absent from all text forms. v5 validates this hypothesis by context analysis of every hit — and discovers that **3 of 5 are actually present** in compound or sandhi-blurred forms that require morphological parsing to detect.

## Validation results

### uK (उक् = u ṛ ḷ) — CONFIRMED VIRTUAL

The only hits are "उकञ्" at 3.2.154. This is NOT the pratyāhāra uK — "उकञ्" is a suffix name (uk + ñ it-marker). Pāṇini uses iK (i u ṛ ḷ) as the superset, never uK. **Confirmed virtual.**

### caY (चय् = k p c ṭ t) — CONFIRMED VIRTUAL

All 5 "चय" hits are inside the word "समुच्चय" (samuccaya = "collection/totality"). This is an ordinary Sanskrit word, not a pratyāhāra reference. Pāṇini uses KaY (kh ph c ṭ t k p) as the superset. **Confirmed virtual.**

### NaM (ङम् = ṅ ṇ n) — NOT VIRTUAL (detection failure)

Sūtra 8.3.32: `ङमो ह्रस्वादचि ङमुण्नित्यम् ।`

Parsing: ङमः (genitive) + ह्रस्वात् (ablative "from short") + अचि (locative "before vowel") + ङम् (stem) + ऊण् + नित्यम् ("always")

Translation: "Of [the class] NaM (ṅ ṇ n), from a short [vowel], before a vowel (aCi), NaM is always [replaced by] ūṇ"

NaM appears **twice** in this sūtra: once in genitive sandhi form (ङमो) and once in citation stem form (ङम्). The pipeline detected aC (अचि) but missed both occurrences of NaM. **Detection failure — sandhi form not recognized.**

### Jaz (झष् = jh bh gh ḍh dh) — NOT VIRTUAL (detection failure)

Sūtra 8.2.37: `एकाचो बशो भष् झषन्तस्य स्ध्वोः ।`

"झषन्तस्य" = Jaz + anta + sya (genitive) = "of [a stem] ending in Jaz"

This is a compound form where the pratyāhāra is the first member of a bahuvrīhi compound. The pipeline missed it because "झषन्तस्य" is a single orthographic word. **Detection failure — compound form not recognized.**

### baS (बश् = b g ḍ d) — NOT VIRTUAL (detection failure)

Same sūtra 8.2.37: "बशो" = sandhi form of बशः = genitive singular of baS.

"बशो" appears as a standalone token (preceded by space, followed by space) — but it's in sandhi form (visarga → o before voiced consonant), so the v6 declined-form detector searched for "बशः" but not "बशो". **Detection failure — visarga sandhi not handled.**

## BONUS: Baz (भष् = bh gh ፡ḍh dh) also at 8.2.37

Sūtra 8.2.37 contains "भष्" in virama form — this IS the pratyāhāra Baz, and it should have been detected by the v5.1 pipeline's structural triggers. But 8.2.37 was classified as MAYBE with no opaque_classes. **Detection failure — pipeline bug.**

## The golden sūtra: 8.2.37

`एकाचो बशो भष् झषन्तस्य स्ध्वोः ।`

This single sūtra contains **three** pratyāhāras, all missed by the pipeline:
1. baS (बशो = genitive, sandhi form)
2. Baz (भष् = virama form — should have been detected!)
3. Jaz (झषन्तस्य = compound form)

Plus the term "एकाचो" (ekāco = genitive of ekāc = "one-vowel") which contains aC as part of a compound.

## aT (अट्) — also a detection failure

Sūtra 8.4.2: `अट्कुप्वाङ्नुम्व्यवायेऽपि ।`

"अट्कु..." = aT + ku... — the pratyāhāra aT is in conjunct form (virama consonant followed by another consonant without space). The pipeline classified this as YES but didn't identify aT. **Detection failure — conjunct form not recognized.**

## Revised effective target and recall

| Category | Count | Explanation |
|:---|:---|:---|
| Canonical 41 | 41 | Wikipedia/traditional sources |
| Minus phantoms | -2 | EC (ऐच्), YaM (ञम्) — absent from all text |
| Minus confirmed virtual | -2 | uK (उक्), caY (चय्) — formable but never used |
| **Effective target** | **37** | Pratyāhāras Pāṇini actually uses in text |

| Detection method | Count | Cumulative |
|:---|:---|:---|
| v5.1 structural triggers | 21 | 21 |
| v6 declined-form detector | +9 | 30 |
| v5 compound/sandhi analysis (this report) | +5 | 35 |
| **Total detectable** | **35** | |
| Remaining misses | 2 | See below |

**Recall: 35/37 = 94.6%** (with all detection methods combined)

## The 2 remaining misses

Of 37 effective target pratyāhāras, 35 are now detectable. The 2 remaining are:

Need to identify which 2 of the 37 are not yet detected by any method. Let me compute:

- v5.1 detected: 22 canonical (including EC phantom) → 21 real
- v6 added: 9 → total 30 real
- v5 analysis added: NaM, Jaz, baS, Baz, aT → total 35 real
- 37 - 35 = 2 remaining

The 2 remaining misses are pratyāhāras that are:
- In the canonical 41
- Present in the text (not phantom)
- Not virtual (actually used)
- Not detected by v5.1, v6, or this analysis

These require a complete cross-check of all 37 against all detection results.

## Sūtra 8.2.37 as a diagnostic test case

The fact that 8.2.37 was classified as MAYBE (not YES) despite containing 3+ pratyāhāras suggests the structural trigger pipeline has a systematic weakness with sūtras that pack multiple pratyāhāras into a single orthographic word via sandhi and compounding.

## Epistemic status

PRELIMINARY ANALYSIS (v5). Superset hypothesis partially falsified: 3 of 5 "virtual" pratyāhāras are actually used. Effective target revised from 34 to 37. Recall estimated at 35/37 = 94.6% with all methods combined. The 2 remaining misses need identification.
