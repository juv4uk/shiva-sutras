# v6.1 Detection Results: Automated Extended Form Recognition

**Date:** 2026-09-07
**Tool:** declined_form_detector_v6_1.py
**Input:** candidate-phonological-rules.yaml (v5.1, frozen)
**Output:** candidate-phonological-rules-v6_1.yaml (supplementary)
**Runtime:** 0.2 seconds (fully automated, no manual annotation)

## Summary

| Metric | v5.1 (structural) | v6.1 (extended) | Delta |
|:---|:---|:---|:---|
| Canonical matched | 22 | 37 | +15 |
| Recall (text-present) | 22/39 = 56.4% | 37/39 = 94.9% | +38.5% |

## Detection patterns

The v6.1 detector extends v6 with three new automated patterns:

### 1. Visarga sandhi (ः → o before voiced)
When a pratyāhāra in genitive (ः) is followed by a voiced consonant in continuous text, the visarga becomes o (ो matra).

Examples:
- बशः + भ → बशो (baS at 8.2.37)
- ङमः + ह → ङमो (NaM at 8.3.32)
- झयः + ह → झयो (JaY at 8.4.62)

### 2. Compound -anta (pratyāhāra + अन्त)
A pratyāhāra stem + अन्त (anta = "ending in") forms a compound meaning "that which ends in [pratyāhāra]". This appears as a sub-string in longer compounds.

Example:
- झषन्तस्य = Jaz + anta + sya (genitive) = "of [that which] ends in Jaz"

### 3. Conjunct (stem + virama + suffix cluster)
A pratyāhāra stem with virama directly followed by a known Pāṇinian suffix marker (कु, वा, ङ्, नुम्, प्वा, ङ्नुम्) without intervening space.

Example:
- अट्कु = aT + ku (at 8.4.2)

## New detections: 15 new canonical pratyāhāras

### Citation form (bare stem, standalone)
- इच् at 6.3.68: `इच एकाचोऽम्प्रत्ययवच्च`
- शल् at 3.1.45: `शल इगुपधादनिटः क्सः`

### Locative (stem + ि)
- अट् at 8.3.3: `अटि नित्यम्`
- अम् at 6.1.107: `अमि पूर्वः`
- इच् at 6.1.104: `इचि`
- खय् at 8.3.6: `खयि अम्परे`
- छव् at 8.3.7: `छवि अप्रशान्`
- झश् at 8.4.53: `झशि`
- यम् at 8.4.64: `यमि लोपः`
- वश् at 7.2.8: `वशि कृति`

### Genitive (stem + ः)
- इण् at 3.3.38: `इणः`
- खय् at 7.4.61: `खयः`
- चर् at 1.3.53: `चरः` (see note below)
- झय् at 5.4.111: `झयः`
- झष् at 8.2.40: `झषः`
- यम् at 1.3.56: `यमः`
- वश् at 6.1.20: `वशः`

### Visarga sandhi (stem + ो)
- अम् at 7.1.40: `अमो मश्`
- इण् at 2.4.45: `इणो गा`
- ङम् at 8.3.32: `ङमो ह्रस्वादचि`
- झय् at 8.4.62: `झयो होऽन्यतरस्याम्`
- बश् at 8.2.37: `बशो भष्`
- यम् at 1.2.15: `यमो गन्धने`

### Dative (stem + े)
- अक् at 6.2.73: `अके जीविकाऽर्थे`
- मय् at 4.4.138: `मये च`
- वल् at 6.3.118: `वले`

### Conjunct (stem + virama + suffix)
- अट् at 8.4.2: `अट्कुप्वाङ्नुम्व्यवायेऽपि`
- अश् at 4.1.110: `अश्वादिभ्यः` (NOTE: this is likely the word "aśva" = horse, NOT the pratyāhāra aS — see below)

## Notes on ambiguous detections

### छवि at 8.3.7 — pratyāhāra CaW or word "छवि" (sprinkling)?

The padaccheda splits "नश्छव्यप्रशान्" as "नः छवि अप्रशान्", confirming "छवि" is a standalone token. In the phonological context of 8.3.x (sandhi rules), this is likely the pratyāhāra CaW (coronal voiceless stops: ch ṭh th c ṭ t) in locative = "in [the context of] CaW". The alternative reading (छवि = sprinkling) is possible but less likely in a phonological rule context.

**Status: AMBIGUOUS — likely pratyāhāra but not certain.**

### चरः at 1.3.53 — pratyāhāra caR or root चर् (to move)?

The padaccheda splits as "उदः चरः सकर्मकात्". In the context of 1.3.x (verb rules), "उदः" and "चरः" could be root genitives (roots ud and car listed for a verb operation). "सकर्मकात्" (from intransitive) describes verb properties, not phonological classes.

**Status: LIKELY FALSE POSITIVE — probably root genitives, not pratyāhāra.**

If चरः is excluded: 37 - 1 = 36 canonical matched, recall = 36/39 = 92.3%.

### अश्वा at 4.1.110 — pratyāhāra aS or word "अश्व" (horse)?

"अश्वादिभ्यः" = अश्व + आदिभ्यः = "from horse etc." — this is the word "aśva" (horse), NOT the pratyāhāra aS. The conjunct detection matched "अश् + वा" but "अश्वा" is actually "अश्व" + "आ" (vowel elongation).

**Status: FALSE POSITIVE — word "aśva", not pratyāhāra aS.**

If अश्वा is excluded: the aS pratyāhāra was already detected by v5.1, so this doesn't change the canonical count.

## Effective automated recall

| Scenario | Matched | Recall |
|:---|:---|:---|
| v6.1 raw | 37/39 | 94.9% |
| v6.1 minus चरः false positive | 36/39 | 92.3% |
| v6.1 minus both ambiguous | 35/39 | 89.7% |

Even in the most conservative scenario (excluding both ambiguous detections), automated recall is **89.7%** — just below the 90% threshold.

## Epistemic status

ENGINEERING tool. Fully automated — no manual annotation.
Runtime: 0.2 seconds. All detections are blind (pattern-based).
The v5.1 frozen harvest is NOT modified. v6.1 produces a supplementary YAML.
Two ambiguous detections require owner adjudication.
