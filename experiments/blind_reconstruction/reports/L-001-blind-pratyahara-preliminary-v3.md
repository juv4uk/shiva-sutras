# L-001 Preliminary v3: Corrected Canonical Baseline & Disambiguation Analysis

**Status:** PRELIMINARY ANALYSIS (v3 — supersedes v2)
**Date:** 2026-09-07
**Analyst:** Sarvam AI agent
**Data source:** `ksetra/astadhyayi/blind/candidate-phonological-rules.yaml` (Stage 6.0B, 3983 sūtras)
**Sources:** Wikipedia "Shiva Sutras" (citing traditional grammar), Ananthanarayana (1971), Kiparsky (1991), appliedsyntax.com

## Correction from v2

The v2 report used a flawed "canonical 42" list that included invalid pratyāhāras and missed valid ones. The v3 analysis uses the authoritative list of 41 pratyāhāras that Pāṇini actually uses in the Aṣṭādhyāyī, as documented by traditional grammar and confirmed by Wikipedia [cite:097bad31] and Ananthanarayana [cite:bc21aa00].

### Key corrections

1. **saR (सर्) REMOVED** — This is a single-element pratyāhāra ({s} only). Pāṇini never uses single-element pratyāhāras (well-established principle). All 118 "सर्" hits in the text are parts of ordinary words (सर्व, उपसर्ग, उपसर्जन). **Zero** are pratyāhāra references.

2. **yaV (यव्) REMOVED** — Not in the standard 41 list. Pāṇini uses yaÑ and yaṆ (both = y,v,r,l) but never yaV.

3. **10 pratyāhāras ADDED** that were missing from v2's list: śaL (शल्), jhaY (झय्), jhaṢ (झष्), bhaṢ (भष्), baŚ (बश्), caY (चय्), caR (चर्), iṆ (इण्), uK (उक्), iC (इच्)

## Corrected Results

### Precision: 20/22 = 90.9%

The blind pipeline detected 22 unique markers. Of these:
- **20 are true positives** (in the canonical 41, present in text)
- **1 is a phantom match** (ऐच्/EC — in canonical 41 but absent from text entirely; likely anuvṛtti-only)
- **1 is valid but not in Wikipedia's 41** (अक्/ak — recognized by Ananthanarayana as used by Pāṇini)

### Recall: 20/39 = 51.3%

Of the 41 canonical pratyāhāras:
- **39 appear in the Aṣṭādhyāyī text** (with or without virama)
- **2 are absent from the text** (ऐच्/EC, ञम्/YaM — likely anuvṛtti-only or phantom)
- Of the 39 present, the pipeline detected **20**

## The 18 present-but-undetected pratyāhāras

| Pratyāhāra | Has virama form? | Form in text | Root cause |
|:---|:---|:---|:---|
| अट् (aT) | Yes (1 hit) | 8.4.2 | Low frequency, single occurrence |
| अम् (aM) | Yes (4 hits) | Multiple | Common syllable (am = "this/that") |
| इच् (ic) | Yes (5 hits) | Multiple | Common substring |
| इण् (iR) | Yes (3 hits) | Multiple | Ambiguous with इण् (this/that) |
| उक् (uk) | **No** (0 hits) | Declined only | Appears only without virama |
| खय् (KaY) | Yes (1 hit) | Rare | Low frequency |
| ङम् (NaM) | **No** (0 hits) | Declined only | Appears only without virama |
| चय् (caY) | **No** (0 hits) | Declined only | Appears only without virama |
| चर् (caR) | Yes (14 hits) | Multiple | "चर्" is also the root "to move/wander" |
| छव् (CaW) | Yes (1 hit) | 8.3.7 | Low frequency |
| झय् (JaY) | **No** (0 hits) | Declined only | Appears only without virama |
| झश् (JaS) | **No** (0 hits) | Declined only | Appears only without virama |
| झष् (Jaz) | **No** (0 hits) | Declined only | Appears only without virama |
| बश् (baS) | **No** (0 hits) | Declined only | Appears only without virama |
| भष् (Baz) | Yes (1 hit) | Rare | Low frequency |
| यम् (yaM) | Yes (32 hits) | Multiple | "यम्" = root "to restrain" + common syllable |
| वश् (vaS) | Yes (19 hits) | Multiple | "वश्" = root "to wish/choose" + common syllable |
| शल् (SaL) | **No** (0 hits) | Declined only | Appears only without virama |

### Root cause classification

| Root cause | Count | Pratyāhāras |
|:---|:---|:---|
| Appears ONLY in declined form (no virama) | 8 | uK, NaM, caY, JaY, JaS, Jaz, baS, SaL |
| Common syllable / homonym conflict | 6 | aM, iR, caR, yaM, vaS, iC |
| Low frequency (1-2 hits) | 4 | aT, KaY, CaW, Baz |

### Critical insight: the declined-form blind spot

**8 of 18 missed pratyāhāras appear ONLY without virama** in the Aṣṭādhyāyī text. The structural trigger pipeline searches for virama forms (e.g., "शल्") but these pratyāhāras appear exclusively in declined forms (e.g., "शलि" = locative of śaL). This is a **systematic blind spot** in the pipeline — not a random failure.

In Pāṇinian sūtra style, a pratyāhāra is typically cited in a declined form:
- Locative: "शलि" = "in [the class] śaL" (most common)
- Genitive: "शलः" = "of śaL"
- Ablative: "शल्मात्" = "from śaL"

The citation form with virama (शल्) appears only in lists and enumerations, not in operational rules.

## The "sar" red herring

The v2 report identified "सर्" (sar) as a high-frequency miss (129 hits). The v3 analysis reveals this was entirely a false alarm:

- **0 of 118 virama hits** are pratyāhāra references — all are parts of words (सर्व=sarva, उपसर्ग=upasarga, etc.)
- saR is a single-element pratyāhāra ({s}) that Pāṇini never uses
- The structural pipeline was correct to NOT flag these as pratyāhāras

Similarly, "यव्" (yaV, 64 hits) was a false alarm — yaV is not in the 41 canonical pratyāhāras, and all hits are ordinary syllables.

## Revised Summary

| Metric | v2 (incorrect) | v3 (corrected) |
|:---|:---|:---|
| Target set | 38 (wrong) | 41 (authoritative) |
| Present in text | 33 (wrong) | 39 |
| Absent from text | 5 (wrong) | 2 (ऐच्, ञम्) |
| True positives | 17 | 20 |
| False positives | 1 | 2 (ऐच् phantom, अक् not-in-41) |
| **Precision** | 81.8% | **90.9%** |
| **Recall** | 51.5% | **51.3%** |

## Implications for L-001

1. **The effective target is 39, not 33 or 42.** Two pratyāhāras (ऐच्, ञम्) are absent from the text entirely — likely anuvṛtti-only or phantom.

2. **The declined-form blind spot is the #1 recall problem.** 8 of 18 misses (44%) are pratyāhāras that appear ONLY without virama. The pipeline must learn to recognize declined pratyāhāra forms (locative -i, genitive -aḥ, ablative -māt).

3. **Homonym disambiguation is the #2 problem.** 6 of 18 misses (33%) are pratyāhāras that are also common Sanskrit syllables/roots (यम्=restrain, वश्=wish, चर्=wander). Distinguishing pratyāhāra usage from ordinary usage requires semantic context.

4. **Low-frequency pratyāhāras** (4 of 18, 22%) appear only 1-2 times — these need targeted detection, not broad-pattern matching.

5. **The "129 hits for sar" problem was a red herring.** It was never a recall failure — it was a false entry in the test set.

## Epistemic Status

PRELIMINARY ANALYSIS (v3, corrected). The canonical baseline is now authoritative (41 pratyāhāras per Wikipedia/traditional sources). No outcome class assigned. L-001 run is ACTIVE (run_started_at = 2026-09-06) but not complete.
