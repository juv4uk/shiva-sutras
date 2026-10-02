# The language-faithful 7-bit table (candidate, research, hypothesis)

Owner's requirement (2026-10-02): the projection must correspond to the language: **switch the layout to Ukrainian and you write Ukrainian words; switch it to Sanskrit and you write Sanskrit words.**

Files: `prototype/upc7_lang.py` (the layer), `prototype/uk_orth.py` (Ukrainian orthography <-> sounds), `prototype/build_v3_table.py`, `prototype/upc7-table-v3.tsv` (the table, 93 rows), `prototype/test_upc7_lang.py`.
The pinned `upc7-table.tsv` (which SENS pins by sha) is **not changed**.

## 1. The model

A cell is a **sound**. A layout is how a language writes it. Four layouts: `sa-iast`, `sa-deva` (real Devanagari: consonant + virama, vowel signs, inherent a), `sa-cyr` (Sanskrit in Ukrainian letters, the scheme of the owner's book), `uk` (Ukrainian orthography). The cell stream is the same in all of them; `switch(text, from, to)` changes only the human projection.

```text
кіт  --uk-->  3 cells  --sa-iast-->  kit      --sa-deva-->  कित्
योग  --sa-deva-->  4 cells  --sa-iast-->  yoga   --sa-cyr-->  йоґа
жито --uk--> 4 cells --sa-iast--> REFUSED  (Sanskrit has no ж)      kṛṣṇa --sa-iast--> uk REFUSED (no ṣ, ṛ)
```

A sound the other language does not have has **no spelling there and is refused** (`UnrenderableCode`), never approximated.

## 2. Which sounds are shared (the pinned table's own decision, kept)

16 Ukrainian letters name the same sound as a Sanskrit letter: к=k ґ=g т=t д=d н=n п=p б=b м=m і=i у=u й=y с=s р=r л=l в=v ш=ś.
14 sounds are Ukrainian-only (own cells): ж з ф х г ц ч дз дж ь а е о и. 55 cells are Sanskrit (the 42 sounds, ā ī ū ṝ, 9 nasal vowels), derived from the UPC-14 graph (`upc7_derive`); 27 are signs.
Not decided by me, the owner's call: the pinned table keeps Ukrainian а е о и apart from Sanskrit a e o (UPC-8 calls them "near-equivalent"), and merges ш with ś and л with l.

### 2a. What the phonetic comparison says about those inherited merges (the shiva agent, `docs/sanskrit-ukrainian-sounds-2026-10-02.md`, PR #76; Sanskrit places and voicing source-confirmed from the Laghukaumudī, IPA symbols an external convention)

- **Unambiguously one sound:** i/і, u/у, k/к, g/ґ, y/й, p/п, b/б, m/м, t/т, d/д, n/н (both dental), s/с: the shared cells are right.
- **Close, not identical; the pinned table nevertheless puts them in ONE cell and this candidate keeps that:** r/р, l/л (Ukrainian л is a hard ɫ plus a separate soft one), v/в, ś/ш (Sanskrit has ś and ṣ, Ukrainian one ш). **Different in quality and kept apart in the pinned table (separate cells): a/а, e/е, o/о** (the Sanskrit short a is saṃvṛta in use; e, o are long). The pinned table merges r/р, l/л, v/в, ш/ś; whether to split r/р, l/л, v/в, ш from ś/ṣ is the owner's decision (splitting would give each its own cell; nothing in the layer needs the merge).
- **h is Ukrainian г [ɦ]** by the Laghukaumudī (voiced, aspirated, throat), not х [x]; the pinned table has h and г as two cells; this candidate keeps them two (h moves, г does not). **Tension, for the owner:** the model says a cell is a sound, and h and г are the same sound [ɦ]; two cells for one sound contradicts it, while the book writes Sanskrit h as х, not г. Either г shares the cell of h (and the Sanskrit-Cyrillic layout writes it х) or the two stay apart by decision; not resolved here.
- **Sanskrit-only (refused in `uk`):** aspirates, ṭ ḍ ṇ, ṅ ñ, ṛ ḷ, the long vowels; **Ukrainian-only (refused in the Sanskrit layouts):** и ж з ц ф х дз щ and the soft consonants.

## 3. The Ukrainian orthography (stated as code, `uk_orth.py`)

| orthography | sounds |
|---|---|
| я ю є after a consonant | consonant + ь (softness) + а у е |
| я ю є at a word start or after a vowel | й + а у е |
| ї | й + і |
| щ | ш + ч |
| ь, `ьо`, `йо` | softness; ь + о; й + о |
| `'` before я ю є ї after a consonant | consonant + й + vowel (the apostrophe is re-inserted on rendering) |
| дз дж ц ч | one cell each |

**Evidence (executable, `DictionaryTests`):** 229,973 Ukrainian lemmas of `dict_uk` (`base.lst`) go through `to_orth(to_tokens(w))`: **229,939 round-trip exactly (99.985%)**; 26 differ and 8 are refused.
The 26 are **two classes** (found by the independent oracle of the panini agent, who split them): **21** are a **й or ь + vowel across a morpheme boundary** (13 with й: райавтодор, райагробуд, райелектромережа, натрійурез; 8 with ь: бельетаж, сільуправа, гідромідьустановка, утильустановка), where the sounds do not say whether the letters are `йа` or `я`, `ьу` or `ю`; no phoneme-level layer can know that without morphology. **5** are `ш + ч` that comes back as `щ` (батюшчин, пляшчина, пляшчинка, подушчаний, шарашчин): `щ` = ш + ч is ambiguous the other way. The 8 refused are colloquial words with an apostrophe not before я ю є ї (чо', пра').

**Independent check:** the panini agent wrote her own transducer from the rule table above (`uk_orth.py` unread) and ran it on all of `base.lst`: classification identical in every row (232,032 exact, 26 differ, 7,130 refused: hyphenated and tagged lines, not pure Cyrillic words, plus the 8); the token sequences are identical on all 232,058 words where both give tokens. This confirms the implementation of the table, **not** the table against real orthography (both come from the same table).

## 4. What changes in the table (candidate vs pinned)

Of 93 cells: 84 are the same, 9 are the same cells that had no spelling in the pinned table (nasal vowels), and **3 move**: Sanskrit h `0110100 -> 0100001`, r `0101110 -> 0101010`, l `0101111 -> 0101110`. Ukrainian р and л share the cells of r and l, so they move with them. This is the same migration the SENS side described (a Text-identity change: lock bump, regenerated projection, silent shift of existing bytes `0x2E`: r becomes l). It is not applied here.

## 5. Not done (do not read more into it)

- **Case (added into free cells).** Cell `0111000` (`capital`, non-varga place 6) means "the next letter is uppercase"; written by the Ukrainian layout only (`Україна` round-trips); Sanskrit layouts are lowercase and refuse a capital. `fold_case` is no longer needed for round-trip, but still a possible input mode.
- **Stress (added).** Cell `0111001` = combining acute after a vowel (`дя́дя`), Ukrainian layout only.
- **Sanskrit signs (added).** anusvāra, visarga, avagraha, daṇḍa, double daṇḍa use the five sign cells the pinned geometry already had (`1101000`–`1101100`); spelled ṃ ḥ ’ । ॥ (IAST), ं ः ऽ । ॥ (Devanagari), м̇ х̣ ’ । ॥ (Cyrillic). Refused in the Ukrainian layout.
- **Long nasal vowels (added)**: ā̃ ī̃ ū̃ ṝ̃, four free vowel-class cells.
- **Still no cell:** punctuation outside ASCII (`—`, `«»`, `…`; refused) and pluta. Free after this: varga 7, non-varga 12, vowel 2 (ḹ-related, do not exist), sign 0. Using the free varga/non-varga cells for punctuation would break the class semantics (a "consonant" cell that is a dash): a decision for the owner.
- **Ukrainian morphology**: the й + vowel ambiguity of §3; the orthography is not checked against an independent Ukrainian orthography oracle (requested from the panini agent).
- The shared-sound decisions of §2 are inherited, not re-derived; the shiva agent was asked for a source-checked phonetic comparison (IPA, source, confidence) of the borderline pairs (а/a, г/h, р/r, л/l, ш/ś, в/v).
- CI: not run.

## 6. Коротко українською

Клітинка це **звук**, розкладка це спосіб записати його мовою. Переключили українську: пишете українські слова (я ю є ї щ, ь, апостроф), санскритську (IAST, справжня деванагарі, санскрит кирилицею за книгою): санскритські.
Звуку, якого нема в іншій мові, у тій розкладці немає запису, і він відхиляється, а не наближається. На 229 973 українських лемах `dict_uk` 99,985% повертаються точно, 26 різняться
через «й або ь + голосна» на межі морфем (21) та «шч → щ» (5), 8 відхилено (розмовні апострофи). Порівняно з закріпленою таблицею рухаються три клітинки (h, r, l, українські р і л разом із r і l): це та сама міграція SENS Text7, яку тут не застосовано.
Не зроблено: регістр (великі літери), пунктуація поза ASCII, анусвара/вісарга/плута, наголос.
