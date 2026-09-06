# Declined-Form Detection Results (v6 post-processing pass)

**Date:** 2026-09-07
**Tool:** declined_form_detector.py
**Input:** candidate-phonological-rules.yaml (v5.1, frozen)
**Output:** candidate-phonological-rules-v6.yaml (supplementary)

## Summary

| Metric | v5.1 (structural) | v6 (+declined) | Delta |
|:---|:---|:---|:---|
| Canonical matched | 22 | 31 | +9 |
| Recall (text-present) | 22/39 = 56.4% | 31/39 = 79.5% | +23.1% |

Note: v5.1 had 22 canonical matches (not 20 as previously reported — the v5.1 opaque_classes field contains some entries that were counted differently in v3/v4). The v6 pass adds 9 new canonical pratyāhāra detections via declined/citation form recognition.

## New detections (9 new canonical pratyāhāras)

### śaL (शल् = ś ṣ s h, fricatives)
- Form found: `शल` (citation, bare stem at sūtra start)
- Context: `शल इगुपधादनिटः क्सः ।`
- Sūtra: 3.1.45
- Status change: maybe → yes

### JaS (झश् = jh bh gh ḍh dh j b g ḍ d, voiced oral stops)
- Form found: `झशि` (locative singular)
- Context: `झलां जश् झशि ।`
- Sūtra: 8.4.53
- Status change: yes (already) → added to opaque_classes

### JaY (झय् = all oral stops)
- Form found: `झयः` (genitive singular)
- Context: `झयः ।`
- Sūtras: 8.2.10, 5.4.111
- Status change: no/maybe → maybe/yes

### iR (इण् = non-open continuants)
- Form found: `इणः` (genitive singular, multiple occurrences)
- Context: `दीर्घ इणः किति ।` and `इणः षः ।`
- Sūtras: 6.1.107(?), 8.2.36(?), 8.2.37(?)
- Status change: various → yes

### yaM (यम् = resonants)
- Form found: `यमः` (genitive singular) and `यमि` (locative singular)
- Context: `यमः समुपनिविषु ।` and `हलो यमां यमि लोपः ।`
- Status change: no → maybe (genitive), yes (locative)

### vaS (वश् = voiced consonants except y)
- Form found: `वशः` (genitive) and `वशि` (locative)
- Context: `न वशः ।` and `नेड् वशि कृति ।`
- Status change: maybe → yes

### aM (अम् = voiced sonorants)
- Form found: `अमि` (locative singular)
- Context: `अमि पूर्वः ।`
- Status change: maybe → yes

### iC (इच् = non-open syllabics)
- Form found: `इच` (citation form)
- Context: `इच एकाचोऽम्प्रत्ययवच्च ।`
- Status change: maybe → yes

### KaY (खय् = voiceless stops)
- Form found: `खयः` (genitive singular)
- Context: `शर्पूर्वाः खयः ।`
- Status change: maybe → yes

## Additional re-detections (already canonical, found in new forms)

The script also found declined forms of pratyāhāras that were already detected by v5.1 (e.g., eC, hal, aC, maY, aK in citation form). These confirm v5.1 detections but don't add new canonical matches.

## Methodology

1. Built declined forms for all 41 canonical pratyāhāras (locative -i, genitive -aḥ, ablative -māt, dative -e, accusative -o)
2. Searched continuous `source_text` (not just `padaccheda`) for standalone declined forms
3. Also searched for citation forms (bare stem at sūtra start, standalone token)
4. Filtered: only standalone tokens (preceded by space/start, followed by space/danda/visarga/end)
5. Skipped forms already in v5.1 opaque_classes

## Remaining 8 undetected pratyāhāras

After v6, 8 of 39 text-present canonical pratyāhāras remain undetected:

| Pratyāhāra | In text? | Why missed |
|:---|:---|:---|
| aT (अट्) | Yes (1 hit, 8.4.2) | Low frequency, virama form exists but pipeline didn't flag |
| uK (उक्) | Likely anuvṛtti-only | Virtual (superset: iK) |
| NaM (ङम्) | Likely anuvṛtti-only | Virtual (superset: yaM) |
| caY (चय्) | Likely anuvṛtti-only | Virtual (superset: KaY) |
| Jaz (झष्) | Likely anuvṛtti-only | Virtual (superset: JaS) |
| baS (बश्) | Likely anuvṛtti-only | Virtual (superset: jaS) |
| EC (ऐच्) | Absent | Phantom/anuvṛtti-only |
| YaM (ञम्) | Absent | Phantom/anuvṛtti-only |

If the 5 "virtual" pratyāhāras are confirmed as never explicitly used, the effective target becomes 34, and recall becomes **31/34 = 91.2%**.

## Epistemic status

ENGINEERING tool. Does not modify the frozen v5.1 harvest. Produces supplementary v6 YAML for analysis.
The v6 YAML should NOT be used as the basis for L-001 outcome determination without owner review.
