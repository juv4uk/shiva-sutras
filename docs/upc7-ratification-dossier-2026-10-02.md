# Sound7 / UPC-7 candidate v3 — ratification dossier (prepared, NOT ratified)

Author: claude-sonnet-5-5 (coordinator). Status: **draft for the owner**. Nothing here is decided; every item names its evidence rung (§3a of the root policy: local run < clean CI < reproducible CI test < independent external reproduction) and what is NOT checked.

## 1. What would be ratified

The candidate table `prototype/upc7-table-v3.tsv` (117 of 128 cells; `docs/upc7-language-table-2026-10-02.md`), as the language-aware projection of the UPC-14 sound graph: a cell is a SOUND, a layout is the way a language writes it; a sound the language does not have is refused, never approximated. The pinned table (sha256 dbceb273…ccca6) is untouched; v3 differs from it only by h r l (moved) and by the added cells below.

## 2. Symbols present in BOTH the Sanskrit and the Ukrainian layouts (the owner's question)

Total 53 shared cells: 16 letters + 10 digits + 27 ASCII signs.

### 2.1 Sixteen letters
| Ukrainian | Sanskrit (IAST) | judgement (shiva, #76, Laghukaumudī; IPA an external convention) | status |
|---|---|---|---|
| к ґ т д н п б м | k g t d n p b m | one sound (stops, nasals: n both dental) | unambiguous |
| і у й с | i u y s | one sound | unambiguous |
| р л в ш | r l v ś | close, NOT identical (ɫ hard л + soft; Sanskrit ś and ṣ vs one ш) | merge inherited from the pinned table; **owner decision to keep or split** |

Not shared on purpose (separate cells): а/a, е/e, о/o (quality differs), г/h (tension: h = [ɦ] = Ukrainian г by the source, the book writes х; two cells for one sound contradicts "a cell is a sound": **owner decision**), ж з ф х ц ч дз дж ь щ и (Ukrainian only); aspirates, ṭ ḍ ṇ ṅ ñ ṛ ḷ, long vowels (Sanskrit only).

### 2.2 Ten digits 0-9
Text, not Number. Affine placement (cell = base ^ XOR of 4 columns by the digit's bits, 0..9 only), cells 28 31 29 30 56 59 57 58 25 26, all reserved in the pinned table (no migration). Natively written `0-9` (uk, IAST, Cyrillic) and `०-९` (Devanagari). Evidence: tests; panini independent review (my-lisp-panini#45/#46); shiva comparison (#94/#96). Not checked: decode I refs; need for XOR-closure.

### 2.3 Twenty-seven ASCII signs
Space, newline, tab, ( ) " \ _ & | ` + - * / = < > ? ! ' . , : ; # @ — identical cells in every layout (pinned geometry, unchanged). Convention, not generated.

## 3. What the evidence says

| claim | rung | evidence | NOT checked |
|---|---|---|---|
| each shared letter round-trips in all layouts | local runs + CI (upc7 job) | test_upc7_lang; panini round-trip 4 layouts x 400 | independent corpus beyond dict_uk lemmas (99.985% exact; 26 differ by й/ь+vowel at morpheme boundaries, 8 rejected) |
| cell laws are coordinate/representation, not Sound semantics | independent reproduction (panini#47) | relabelling attack E1/E2/E3 | whether G is the full automorphism group |
| no digit cell can be coerced to a Number | independent source read + probe | panini#47 d7_probe; value.rs, arithmetic.rs | sens-host, FASL/JSON/TCP paths; `(number->string <Text7>)` leaks the wire token (unintended inheritance) |
| the merged cells p/р.. are the right sounds | source-confirmed phonetics | LK 1.1.9 etc. | independent phonetician; the book's photos pp. 810-812 only partly used |

## 4. Open decisions (the owner's, not ours)

1. Keep the merges р/r, л/l, в/v, ш/ś, or split them (a split gives each sound its own cell; nothing in the layer needs the merge).
2. h/г: one cell or two.
3. Migrating h, r, l from the pinned cells to the derived ones (saṅkṣepa7) is a **Text-identity migration** for SENS (#1700, #1981): lock bump + regenerated projection + wire/test updates; 273 of 617 Ukrainian literals in SENS contain р/л.
4. Digits' placement (affine within reserved cells) and punctuation outside ASCII (« » — – …: 11 free cells, shiva recommends a reserve).
5. Whether Text7 is renamed Sound7 in code (prose already renamed in tasks).

## 5. Attack plan before ratification (assigned)

- panini: confusables and normalisation (Latin/Cyrillic homoglyphs, NFC/NFD of ś ṛ ṃ, Devanagari digit vs ASCII digit), cross-layout rendering of shared letters, collisions of shared cells with language syntax.
- shiva: phonetic counter-examples for the 16 pairs (minimal pairs whose meaning changes under the shared cell), independent sources for р л в ш.
- Everyone: report claim | evidence rung | command | not checked.
