# Devanagari to IAST Mapping Contract

## 1. Principles
- **Span-Aware Conversion:** Only contiguous blocks of Devanagari characters (`\u0900-\u097F`) are transliterated.
- **Strict Preservation:** All Latin characters, whitespace, digits (non-Devanagari), and punctuation are preserved exactly (byte-identical).
- **Line-Mapping:** 1 source line = 1 derived line.

## 2. Character Classes
- **Devanagari (Transliterated):** `\u0900-\u097F`
- **Preserved (Ignored by Converter):** `A-Z, a-z, 0-9, Punctuation, Whitespace, Extended Latin, etc.`

## 3. Specific Handlings (Non-Bijective & Anomalies)
- **ओं (U+0913 U+0902):** Maps to `oṃ` (NON_BIJECTIVE_FORWARD).
- **ॐ (U+0950):** Maps to `oṃ` (NON_BIJECTIVE_FORWARD).
- **Isolated Dependent Vowels (e.g., `।ि`):** Mapped mechanically (e.g., `|i`). Handled as `UNRESOLVED` conceptually but processed technically.

## 4. Contextual Rules (Standard Sanskrit)
- Inherent `a` is applied to consonants lacking a Virama (`्`) or Mātrā.
- Anusvāra (`ं`) -> `ṃ`.
- Visarga (`ः`) -> `ḥ`.
- Avagraha (`ऽ`) -> `'`.
- Danda (`।`) -> `|`, Double Danda (`॥`) -> `||`.

## 5. Golden Tests
Defined in converter. Validates Bijective, Preserve, and Non-Bijective behaviors.
