# L-001 v4: Declined-Form Detection Analysis & Superset Hypothesis

**Status:** PRELIMINARY ANALYSIS (v4 — extends v3)
**Date:** 2026-09-07
**Analyst:** Sarvam AI agent

## What changed from v3

v3 identified 8 pratyāhāras that appear "ONLY without virama" and classified this as a systematic blind spot. v4 investigates each of the 8 individually and discovers:

1. **3 are actually in the text** — the pipeline missed them due to declined-form blindness
2. **5 are truly absent** from both mūla text and Kāśikā — they may be "theoretically available but never used"

## The 3 detection failures (fixable)

### SaL (शल् = ś ṣ s h, fricatives) — at 3.1.45

Sūtra 3.1.45: `शल इगुपधादनिटः क्सः`

The word "शल" at the start of this sūtra IS the pratyāhāra SaL in citation form (no virama, bare stem with inherent 'a'). The context confirms it: "शल इगुपधादनि" = "for fricatives (śaL) with iK as penultimate, [suffix] aN..."

The pipeline flagged this sūtra as MAYBE (triggers: latent_technical_compound, syntactic_replacement_pattern) but did NOT identify śaL as an opaque class. **This is a detection failure — the pratyāhāra is present but the pipeline doesn't recognize citation forms without virama.**

### JaS (झश् = jh bh gh ḍh dh j b g ḍ d, voiced oral stops) — at 8.4.53

Sūtra 8.4.53: `झलां जश् झशि ।`

The word "झशि" = locative singular of JaS = "in [the class] JaS". The rule says: "JaL [obstruents] become jaS [voiced unaspirated] in JaS [voiced oral stops] context."

The pipeline detected जश् (jaS) but MISSED झश् (JaS), even though "झशि" is right there in a YES sutra. **The pipeline doesn't recognize locative declined forms of pratyāhāras.**

### JaY (झय् = all oral stops) — at 8.2.10 and 5.4.111

Sūtra 8.2.10: `झयः ।` (genitive singular of JaY)
Sūtra 5.4.111: `झयः ।` (same)

"झयः" = JaYaḥ = "of JaY" — the entire sūtra is just the pratyāhāra in genitive case, with the operation coming from preceding sūtras via anuvṛtti.

Both sūtras were classified as MAYBE/NO but the pratyāhāra was not identified. **The pipeline doesn't recognize genitive declined forms.**

### Fix: declined-form detector

All 3 missed pratyāhāras could be detected by a declined-form recognizer:
- **Locative**: pratyāhāra + ि (i) — e.g., झशि = JaS-i
- **Genitive**: pratyāhāra + ः (aḥ) — e.g., झयः = JaY-aḥ
- **Citation**: bare stem without virama — e.g., शल = SaL (standalone at sūtra start)

If implemented, recall would improve from 20/39 = 51.3% to **23/39 = 59.0%**.

## The 5 truly-absent pratyāhāras (superset hypothesis)

These 5 are absent from both the Aṣṭādhyāyī mūla text AND the Kāśikā commentary (in all forms — virama, declined, sandhi):

| Pratyāhāra | Sounds | Superset used instead | Superset detected? |
|:---|:---|:---|:---|
| uK (उक्) | u ṛ ḷ | iK (इक् = i u ṛ ḷ) | YES |
| NaM (ङम्) | ṅ ṇ n | yaM (यम् = ñ m ṅ ṇ n) | YES |
| caY (चय्) | k p c ṭ t | KaY (खय् = kh ph c ṭ t k p) | Present, not detected |
| Jaz (झष्) | jh bh gh ḍh dh | JaS (झश् = jh bh gh ḍh dh j b g ḍ d) | Present, not detected |
| baS (बश्) | b g ḍ d | jaS (जश् = j b g ḍ d) | YES |

**Hypothesis:** These 5 pratyāhāras are listed in the "41" because they are *theoretically available* in the system (the Śiva-sūtra ordering makes them formable), but Pāṇini never explicitly uses them because a superset pratyāhāra always serves his purpose. They are "virtual" pratyāhāras — defined by the system but not instantiated in any rule.

This is the same phenomenon as the v2 phantoms (EC, GaQ, NaR, JaB, YaM), but less obvious because these 5 ARE valid multi-element pratyāhāras (unlike saR which was single-element). They are simply never chosen.

**If confirmed**, the effective target for L-001 drops from 39 to **34** (39 present - 5 virtual), and recall becomes **20/34 = 58.8%** (or **23/34 = 67.6%** with the declined-form fix).

## Revised target breakdown

| Category | Count | Pratyāhāras |
|:---|:---|:---|
| Detected by pipeline | 20 | ac, aR, aL, aS, ik, eN, eC, hal, haS, jaS, JaL, yaY, yaR, maY, raL, vaL, SaR, KaR, JaR, EC(phantom) |
| In text, missed (declined form) | 3 | SaL, JaS, JaY |
| In text, missed (homonym/low-freq) | 11 | aT, aM, iC, iR, KaY, NaM(here?), CaW, caR, Baz, yaM, vaS |
| Truly absent (virtual/superset) | 5 | uK, NaM, caY, Jaz, baS |
| Truly absent (phantom) | 2 | EC, YaM |
| **Total canonical 41** | **41** | |

Note: NaM appears in both "missed" and "virtual" — need to verify. The text has "ङम" without virama (2 hits), which could be the pratyāhāra in declined form OR the ordinary word "ṅama" (name). Context analysis needed.

## Epistemic status

PRELIMINARY ANALYSIS (v4). Three concrete detection failures identified and characterized. Five "virtual" pratyāhāras hypothesized. No outcome class assigned.
