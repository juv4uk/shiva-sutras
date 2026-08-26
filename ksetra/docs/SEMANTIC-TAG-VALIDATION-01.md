# Semantic Tag Validation Report — 2026-08-27

**Status:** WITNESS validation, not a promotion decision

**Validator:** Sakshi (opencode)

**Source:** `corpus_semantic_tags.experiment.jsonl` (287 files, BGE-M3 model)

## Summary

| Metric | Value |
|---|---|
| Files tagged | 287 |
| Unique concepts | 57 |
| Top concept | anumāna (71% of files) |
| Precision on 8-file sample | 37.5% (3/8 correct) |
| Similarity range | 0.55 – 0.66 |
| Downstream use | NONE (tags are pending review) |

## Attractor analysis

| Concept | Frequency | Appropriate for | Problem |
|---|---|---|---|
| anumāna | 205/287 (71%) | Logic, epistemology texts | Over-applied to grammar, medicine, astronomy |
| vākya | 142/287 (49%) | Grammar, linguistics | Too vague; applies to any text with sentences |
| anubhāva | 55/287 (19%) | Aesthetics, performance | Moderate frequency, less problematic |
| virodha | 43/287 (15%) | Logic, debate | Acceptable |
| bheda | 42/287 (15%) | Philosophy, distinction-making | Acceptable |

## Sample validation

| File | Genre | Top Tag | Correct? | Notes |
|---|---|---|---|---|
| hetubinduTIkAloka | Buddhist logic | anumāna | YES | Core subject is inference |
| paribhAShendushekhara | Grammar | anumāna | NO | Grammar text, should be vyākaraṇa |
| shAstradIpikA | Mīmāṃsā | anumāna | QUESTIONABLE | Hermeneutics, not pure inference |
| charakasaMhitA | Ayurveda | anumāna | NO | Medical text, should be oṣadhi |
| Ishvarapratyabhij~nAkArikA | Shaiva philosophy | anumāna | YES | Philosophical reasoning |
| sAMkhyakArikA yuktidIpikA | Sāṃkhya philosophy | anumāna | YES | Philosophical reasoning |

## Root cause

The BGE-M3 anchor set (`v3-bilingual`) has 57 concepts drawn from the Śiva-sūtra epistemological vocabulary. Epistemological terms (anumāna, vākya, pratyakṣa) are inherently broad — they match any text that discusses knowledge, language, or reasoning. The similarity threshold (0.55) is too permissive to discriminate.

## Recommendations

1. **Do not promote these tags to Obsidian or knowledge graph** without manual review
2. **Expand anchor set** with genre-specific concepts (vyākaraṇa, oṣadhi, kāvya, dharma, etc.)
3. **Raise similarity threshold** to 0.65+ for automatic acceptance
4. **Add genre classifier** as first-pass filter before semantic tagging
5. **Manual review** of the 205 anumāna-tagged files for false positives

## Epistemic status

- Precision measurement: CONFIRMED (manual inspection of 8 files)
- Attractor diagnosis: CONFIRMED (71% frequency is mechanical)
- Root cause hypothesis: PARTIAL (anchor set composition needs full audit)
- Recommendation: PROPOSED (requires owner decision)
