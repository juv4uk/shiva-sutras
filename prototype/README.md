# UPC-8 Prototype

> **Status: `experimental` / `engineering`, not a research or hardware result.**
> See `hypotheses/shabda/status.yaml#H2` (`PREMATURE-HYPOTHESIS`). This
> prototype does **not** claim: a historical encoding Pāṇini intended, a
> universal inventory of human phonemes (see `docs/world-phonetics-and-upc.md`
> for why no such finite list exists to claim), or an FPGA performance
> result — it is a pure-Python engineer's sketch, no RTL, no synthesis.
> "Canonical" below means *engineering base code assignment*
> (`canon:code`), not the transmitted canon itself (`canon:transmitted`)
> — see `docs/EPISTEMIC_CONSISTENCY_AUDIT_v1.md` (ECA-007) for why that
> distinction matters.

Universal Phoneme Code — an 8-bit engineering code assignment over the Śiva Sūtras, explored here as a compact representation prototype (not yet targeting any specific hardware).

## Architecture

```
CANON (Śiva Sūtras, immutable)
  └→ Sanskrit interpretation layer (dīrgha, anusvāra, visarga)
       └→ Language extension layers (Ukrainian, English, ...)
            └→ UPC-8 8-bit encoding
```

The Śiva Sūtras are the **canonical core** — 14 sūtras, 43 positions, 42 unique sounds (h appears in both sūtra 5 and sūtra 14, aliased to one code). No modification, no IPA, no features live inside the canon. Everything else is an interpretation or extension layered on top.

## Code Space

| Range      | Layer              | Count | Description                                      |
|------------|--------------------|-------|--------------------------------------------------|
| 0x00–0x29  | Canonical          | 42    | Śiva Sūtra sounds in sequence order              |
| 0x2A–0x30  | Sanskrit extended  | 7     | Long vowels (ā, ī, ū, ṝ, ḹ), anusvāra, visarga   |
| 0x31–0x4F  | Ukrainian          | 31    | Near-equivalent + new-extension phonemes          |
| 0x50–0x7F  | English (reserved)  | —     | Future                                           |
| 0x80–0xFF  | Reserved           | —     | Future languages                                 |

**Total assigned: 80 codes. Reserved: 176 codes.**

Ukrainian also reuses 13 canonical codes (shared sounds like /i/, /u/, /k/, /p/, etc.) — these don't consume new code space.

## Files

- `upc8.py` — encoder/decoder/pratyāhāra engine
- `test_upc8.py` — 28-test suite (all passing)

## Usage

> **Input model (docs/upc8-prototype-deep-review.md#4):** `encode_sanskrit()`
> is a legacy, narrow function — canonical SLP1 plus a small internal
> ASCII placeholder spelling for the extended codes (`"a:"`, `"H"`, ...),
> **not** general Unicode IAST, despite the name. For explicit, honest
> input handling use `encode_sanskrit_slp1_token()` (canonical SLP1 only)
> and `encode_sanskrit_iast_token()` (genuine Unicode IAST — `'ā'`, `'ai'`,
> `'kh'`, `'ñ'`, ...). `encode_sanskrit_word(text, scheme=...)` takes an
> explicit `scheme="SLP1"` (default, char-wise) or `scheme="IAST"`
> (greedy longest-match) instead of guessing.

```python
from upc8 import UPC8

u = UPC8()

# Canonical SLP1 (one character per phoneme, no ambiguity)
code = u.encode_sanskrit_slp1_token('a')     # → 0x00
code = u.encode_sanskrit_slp1_token('K')     # → kh, canonical code

# Genuine Unicode IAST (covers the 42 canonical sounds + 7 extended codes)
code = u.encode_sanskrit_iast_token('ā')     # → 0x2A (long vowel, extended)
code = u.encode_sanskrit_iast_token('ai')    # → same code as SLP1 'E'
code = u.encode_sanskrit_iast_token('kh')    # → same code as SLP1 'K'

# Encode Ukrainian (partial ORTHOGRAPHIC contract — see encode_ukrainian_word's
# own docstring; я/ї/є/ю/apostrophe are NOT covered, raise KeyError on purpose)
code = u.encode_ukrainian('і')      # → 0x01 (shared canonical code)
code = u.encode_ukrainian('ш')      # → 0x3B (new code)

# Encode words
u.encode_sanskrit_word('karma')                    # → b'\x25\x00\x0c\x0f\x00' (scheme="SLP1", default)
u.encode_sanskrit_word('khaga', scheme='IAST')      # → longest-match 'kh' as one token
u.encode_ukrainian_word('джаз')     # → b'\x38\x33\x3a'

# Decode
info = u.decode(0x00)                # → {code: 0, layer: 'canonical', slp1: 'a', sutra: 1, ...}

# Pratyāhāra (natural class expansion)
u.pratyahara('ac')                  # → [0x00, 0x01, 0x02, ...] — all 9 vowels
u.pratyahara('hal')                 # → 33 consonants
u.pratyahara('Sar')                 # → [ś, ṣ, s] — 3 sibilants

# Natural class tests
u.is_vowel(0x00)                    # → True
u.is_stop(0x25)                     # → True (k is a stop)
u.is_sibilant(0x29)                 # → True (s is a sibilant)
```

> **Natural-class scope (docs/claude-review-upc8-manus-proposals-2026-08-18.md#6):**
> `is_vowel()`/`is_consonant()`/etc. above are canonical-only and silently
> return `False` for every extension code — you can't tell "not a vowel"
> from "doesn't apply at this layer" from the boolean alone. For explicit
> layer boundaries, use `canonical_class(code)` (strict Śiva-sūtras,
> empty result for anything else), `phonological_class(code, profile=
> "sanskrit")` (long vowels derive vowel-ness from their short base;
> anusvāra/visarga get explicit `{"anusvara"}`/`{"visarga"}` labels
> instead of silent emptiness), and `language_class(code, language=
> "ukrainian")` (shared codes inherit the Sanskrit segment's class,
> new Ukrainian codes via an explicit vowel-letter set):
>
> ```python
> u.canonical_class(0x00)              # → frozenset({'vowel'})
> u.canonical_class(0x2A)              # → frozenset() -- not canonical, not False-False
> u.phonological_class(0x2A)           # → frozenset({'vowel'}) -- ā derives from short a
> u.phonological_class(0x2F)           # → frozenset({'anusvara'})
> u.language_class(0x33)               # → frozenset({'vowel'}) -- Ukrainian а
> ```

## Pratyāhāra Engine

The pratyāhāra engine implements Pāṇini's 1.1.62–1.1.64 rules:

- **First char** = ādi (start sound, included in the set)
- **Last char** = it (marker, excluded from the set)
- **Range** = all listed sounds from start through the end of the marker's sūtra
- **Marker scan** = left-to-right from the start sound's sūtra (handles markers appearing in multiple sūtras, e.g. Ṇ/R appears in both sūtra 1 and sūtra 6)

| Pratyāhāra | Meaning       | Count | Sounds                          |
|------------|---------------|-------|---------------------------------|
| `ac`       | all vowels    | 9     | a i u ṛ ḷ e o ai au            |
| `hal`      | all consonants| 33    | h y v r ... k p ś ṣ s          |
| `ik`       | close vowels  | 4     | i u ṛ ḷ                        |
| `Sar`      | sibilants     | 3     | ś ṣ s                          |
| `yaR`      | semivowels    | 4     | y v r l                         |

## Key Design Decisions

1. **h aliasing**: h appears in sūtra 5 (position 1) and sūtra 14 (position 1). Both map to code 0x09. The sūtra 14 occurrence is recorded as `alias_sutras: [14]` on the code entry.

2. **Unresolved IPA**: Some phonemes have IPA values that are debated or context-dependent. These are marked `ipa: "unresolved"` with an `ipa_candidates` list, not forced to a single value.

3. **Ukrainian shared codes**: 13 Ukrainian phonemes are segment-equivalent to canonical Sanskrit sounds and reuse their codes. The canonical entry gains a `languages.ukrainian` sub-dict with the Ukrainian letter, IPA, and relation type.

4. **Multi-char letters**: Ukrainian has multi-character letters (дж, дз, ць, дзь, щ, etc.). The encoder uses greedy longest-match to handle them.

## Relation to the Ontology

This prototype implements the encoding/hardware layer of the five-layer architecture:

1. Śiva Sūtra Canon (immutable) ← `siva-sutras.yaml`
2. Academic Interpretation (Sanskrit) ← `sanskrit.yaml`
3. Language Extensions ← `ukrainian.yaml`, `english.yaml`
4. Phonological Dimensions ← `phonological-dimensions-v0.3.yaml`
5. **Encoding/Hardware** ← **this prototype (UPC-8)**
