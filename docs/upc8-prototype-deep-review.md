# Досконалий розбір прототипу UPC-8 у `shiva-sutras`

**Автор:** Manus AI  
**Дата аналізу:** 18 серпня 2026 року  
**Предмет:** `prototype/upc8.py`, `prototype/test_upc8.py`, `prototype/README.md`, `prototype/UPC8-documentation-ua.md`, а також пов’язані canon/epistemic артефакти.

> **Короткий висновок:** UPC-8 — хороший компактний engineering prototype, бо він уже чітко демонструє layered mapping, кодову стабільність, aliasing, невизначені IPA та ідею прatyāhāra як природного класу. Але в його поточному стані це ще не надійний phonological interchange format: у загальному алгоритмі pratyāhāra відтворено систематичну помилку, документація перебільшує IAST/word-encoding support, а код не пов’язаний машинно з authoritative canon і extension registries. Його найбільш правильний статус — **experimental engineering hypothesis**, а не мовний, історичний чи FPGA-result claim.

## 1. Що саме є прототипом

UPC-8 — це чистий Python encoder/decoder, який будує 8-бітний простір кодів із трьох шарів. Перші 42 коди представляють 42 унікальні listed sounds у порядку Śiva Sūtras; сім кодів додають санскритські розширення; 31 код відведений для нових українських одиниць, тоді як 13 українських одиниць reuse canonical codes. Повторний `h` у 14-й сутрі alias-иться до коду першого `h` у 5-й сутрі [1] [2].

| Функція | Реалізація зараз | Реальна цінність |
|---|---|---|
| Canonical table | Hard-coded SLP1 tuples, 43 positions → 42 codes | Дає просту, deterministic engineering assignment. |
| Decode metadata | `code → dict` із layer, SLP1, canon ref, alias і language data | Робить code point inspectable, а не просто числом. |
| Sanskrit extensions | `a:`, `i:`, `u:`, `R:`, `L:`, `~`, `H` | Показує, що кодова схема не зводить все до 14 сутр. |
| Ukrainian extension | Shared canonical entries + `UKRAINIAN_NEW` | Демонструє language-specific overlay замість переписування базового шару. |
| Word encoding | Character-wise Sanskrit SLP1 і greedy Ukrainian longest-match | Працює для вузького, чітко обмеженого subset-у. |
| Natural classes | `pratyahara()`, `is_vowel`, `is_stop`, `is_sibilant`, etc. | Найцікавіша ідея прототипу, але саме тут є systematic correctness defect. |

Архітектурна інтуїція хороша:

```text
transmitted canon
  → academic interpretation
    → language extension
      → engineering code assignment
        → possible hardware representation
```

Особливо правильні три принципи. По-перше, повторний `h` не стирається: його second occurrence зберігається як positional alias. По-друге, `ipa: unresolved` з `ipa_candidates` не маскує невизначеність. По-третє, language extension не змінює базову послідовність, а описує relation (`segment-equivalent`, `near-equivalent`, `new-extension`) [1] [2].

## 2. Найсильніша ідея: інженерний код не підміняє канон

Repository already має окремий `ksetra/canon/siva-sutras.yaml`, який визначає себе як pure IAST canonical data без engineering codes [3]. Це правильна онтологічна межа: переданий текст, його positional refs і UPC byte assignment — не одна й та сама річ.

Прототип, однак, поки що hard-code-ить власну SLP1-копію `SIVA_SUTRAS` та extension tables. Тому він перевіряє свою внутрішню консистентність, але не доводить, що лишається синхронним із current repository canon. У довгостроковій системі саме `ksetra/canon/siva-sutras.yaml` має бути data authority; UPC code assignment має бути **похідним versioned artifact** з явно зафіксованими source revision, transliteration profile та extension registry version.

> **Точне розрізнення:** `SS-05:1` як positional ref належить канону; `0x09` як code point належить engineering assignment. Перше не випливає з другого і не отримує історичного статусу через друге.

Це не лише стилістика. Власний epistemic audit repository уже фіксує high-severity термінологічний ризик: слово *canonical* використовується і для переданого тексту, і для engineering code space `0x00–0x29`, і для математично оптимальної структури [4]. Для UPC варто замінити фрази на кшталт «канонічні коди» на **`engineering base codes`**, **`UPC assignment v0.2`** або `canon:code`, зберігаючи `canon:transmitted` лише для Śiva Sūtras.

## 3. Формальна семантика pratyāhāra

У коректній спрощеній моделі прототипу є три різні об’єкти:

1. `P = (p₁, …, p₄₃)` — **listed sound positions** у 14 сутрах.
2. `M_j` — **it/anubandha marker** кожної сутри, який не є елементом `P`.
3. `C(pᵢ)` — UPC code listed sound position; для повторного `h` два positions мають один code.

Для notation `sμ` реалізація вибирає перше listed occurrence `s`, а marker μ — як перший marker у сутрі з ordinal не меншим за start sūtra. Потім результат має бути всіма listed sounds від start position до останнього listed sound selected marker-sūtra, з deduplication only на рівні **code alias**. У цій flattened representation marker вже не присутній у діапазоні, тому йому не потрібно відповідати додатковим `if`.

Незалежна навчальна довідка формулює той самий принцип: pratyāhāra складається з regular letter та anubandha endpoint; `ac` означає діапазон від `a` до marker `c`, а `hal` — усі consonants from `ha` to the `l` marker [5]. Вона також окремо пояснює duplicate `ha` та повторний `ṇ` marker. Це підтримує position-based, а не spelling-based, модель endpoint-а.

### 3.1 Відтворена алгоритмічна помилка

У [`upc8.py`][1] loop, який уже проходить **лише listed sounds**, виконує:

```python
if sound_slp1 == marker_slp1:
    continue
```

Це помилково: код змішує marker token з listed phoneme, якщо вони мають однакове SLP1 spelling. Але marker-а в `CANON_POSITIONS` узагалі немає. Відтак останній `continue` не виключає marker; він видаляє легітимний phoneme.

| Notation | Очікуваний listed member | Фактичний результат | Причина |
|---|---|---|---|
| `hal` | `l` із sūtra 6 | 32 замість 33 consonants, `l` відсутній | marker `l` у sūtra 14 збігається зі звуком `l`. |
| `ay` | `y` із sūtra 5 | `y` відсутній | marker `y` у sūtra 12 збігається зі звуком `y`. |
| `ar` | `r` із sūtra 5 | `r` відсутній | marker `r` у sūtra 13 збігається зі звуком `r`. |
| `am` | `m` із sūtra 7 | `m` відсутній | marker `m` у sūtra 7 збігається зі звуком `m`. |
| `aY` | `Y`/ñ із sūtra 7 | `Y` відсутній | marker `Y`/ñ у sūtra 8 збігається зі звуком `Y`. |
| `av` | `v` із sūtra 5 | `v` відсутній | marker `v` у sūtra 11 збігається зі звуком `v`. |

Я запустив два рівні перевірки. Наявний standalone suite завершився **20/20 PASS**, але він очікує саме помилковий `hal == 32`, тому тест узгоджений із bug-ом, а не з position-based semantics. Далі я побудував ізольований oracle, який використовує той самий documented earliest-marker resolution, що й implementation, але збирає listed positions без spelling-based skip. Серед **301 API-valid two-token forms** oracle зафіксував **81 mismatch (26.9%)**. Розподіл помилок: `m` — 16, `Y` — 15, `l` — 14, `r` — 13, `v` — 12, `y` — 11.

Це не складна архітектурна проблема. Мінімальний correct fix — прибрати conditional skip і залишити deduplication тільки за `code`. Сильніший fix — представляти `Sound` і `Marker` різними typed objects ще до flattening, тоді semantic collision стане неможливою на рівні моделі.

## 4. Input model: документація ширша за код

README та UA documentation заявляють Sanskrit «SLP1 or IAST», проте фактичний API приймає canonical SLP1 symbols і лише кілька extension spellings на кшталт `a:` [1] [2]. Контрольні виклики показали:

| Вхід | Фактичний результат | Висновок |
|---|---|---|
| `encode_sanskrit("E")` | `0x07` | Canonical SLP1 для `ai` працює. |
| `encode_sanskrit("a:")` | `0x2A` | Внутрішнє extension spelling працює. |
| `encode_sanskrit("ai")` | `KeyError` | IAST diphthong не підтриманий. |
| `encode_sanskrit("ā")` | `KeyError` | Unicode IAST довгий голосний не підтриманий. |
| `encode_sanskrit("ṛ")` | `KeyError` | Unicode IAST vocalic r не підтриманий. |
| `encode_sanskrit("kh")` | `KeyError` | IAST aspirate не підтриманий. |
| `encode_sanskrit_word("kh")` | `25 09` (`k`, `h`) | Word encoder розбиває char-by-char, не SLP1/IAST tokenizer. |
| `encode_sanskrit_word("a:")` | `KeyError` на `:` | Single-token extension не composable у word API. |

Отже, сучасна реалізація має чесно називатися **narrow character-wise SLP1 demo encoder**, а не general Sanskrit/IAST codec. Це нормально для prototype. Потрібно лише зробити API explicit:

```text
encode_sanskrit_slp1_token(token)
encode_sanskrit_iast_token(token)
encode_sanskrit_word(text, scheme="SLP1" | "IAST")
```

Word encoder повинен tokenise-ити longest-match units: для SLP1 — `E`, `O`, `K`, `P`, `C`, `W`, `T`, `G`, `Q`, `D`, `J`, `B`; для IAST — `ai`, `au`, `kh`, `gh`, `ṭh`, `dh`, `ā`, `ṛ` тощо. Unicode normalization form має бути зафіксована contract-ом.

## 5. Ukrainian layer: хороше напрямлення, але ще не мовний codec

Greedy longest-match для `дж`, `дз`, `ць`, `дзь`, `ль` — сильна практична ідея. Він справді кодує `джаз` як три bytes і `льон` як `49 34 12`. Але API не обіцяє і не реалізує універсальну українську орфографічну normalisation: `я`, `ї`, `є`, `ю` і слово `моя` зараз викликають `KeyError`.

Це не обов’язково defect. Система може цілком обрати один із трьох різних контрактів:

| Можливий контракт | Що кодується | Необхідна робота |
|---|---|---|
| Orthographic | Всі українські графеми | Визначити `я/ю/є/ї`, апостроф, м’який знак і composition rules. |
| Phonemic | Нормалізовані segments | Побудувати grapheme-to-phoneme preprocessing або приймати вже phonemic input. |
| Transliteration | Явний Latin/SLP-like stream | Визначити alphabet, longest-match lexer і reversible serialisation. |

Небезпека зараз не у вузькому coverage, а у тому, що `encode_ukrainian_word` назвою обіцяє більше, ніж фактично формалізовано. Так само `decode_bytes()` повертає metadata records, але немає language-contextual `decode_ukrainian_word()`; тест, названий Ukrainian roundtrip, перевіряє лише output length і layer, а не reconstructed word [6].

## 6. Natural classes та розширення

`is_vowel()` і `is_consonant()` визначені через membership у canonical `ac`/`hal`. Тому `0x2A` та `0x2B` (long `a`/`i`) повертають одночасно `False` для vowel і consonant. Це може бути свідомим design decision: pratyāhāra працює лише з immutable canon, тоді як extensions мають власну морфологічну семантику. Але тоді API має сказати саме це.

Зараз можливі щонайменше три семантики, і вони не еквівалентні:

1. `canonical_class(code)` — строго Śiva Sūtras only.
2. `phonological_class(code, profile="sanskrit")` — long vowels derive from short-base membership.
3. `language_class(code, language="ukrainian")` — extension-aware feature registry determines membership.

Такий поділ був би кращий за розширення `is_vowel()` неявними винятками. Він також природно узгоджується з п’ятишаровою ontology, яку документ already описує.

## 7. Hardware claim: перспективна архітектура, не результат

UPC-8 uses an 8-bit interchange assignment, але це **не bitfield execution encoding**. Коди відсортовані за порядком сутр, тому natural class не можна вивести простим `(code & mask) == constant`. Документація сама правильно пропонує інший future hardware route: pre-computed `pratyāhāra → 256-bit bitmap`, де membership є `bitmap[code]` [2].

Це хороший design direction, але його треба називати тим, чим він є. Поточний Python implementation виконує linear scan over fixed canonical list при першому зверненні й cache thereafter. Він не містить RTL, gate-level benchmark, bitmap generator, synthesized ROM cost, timing report або bitwise hardware proof. Окремий `hypotheses/shabda/status.yaml` саме тому має H2 «FPGA Hardware Acceleration (UPC-8)» зі статусом `PREMATURE-HYPOTHESIS` [7].

> З факту, що code space можна перетворити на ROM bitmaps, ще не випливає ні O(1) system-level sandhi resolution, ні історична computational purpose Śiva Sūtras, ні hardware advantage над альтернативним representation.

Найкращий майбутній hardware experiment був би маленьким і чесним: generator бере versioned profile, materialize-ить 256-bit bitmap для конкретного class set, synthesise-ить його як ROM/LUT, вимірює resource/timing на fixed FPGA target і порівнює з baseline lookup. Це був би engineering result з власними scope, evidence та limits.

## 8. Data provenance, versioning і відтворюваність

Найсерйозніший architecture gap — table provenance. Prototype має 80 assigned code points, але binary stream не несе:

- `upc_version` / assignment profile;
- source canon revision or SHA;
- selected Sanskrit/Ukrainian registry revision;
- normalisation/transliteration scheme;
- language/profile context for decoding;
- policy for reserved code ranges and future extension collision.

Без цього той самий byte stream може бути stable only by convention, not by self-describing contract. Для interchange format варто мати хоча б envelope:

```yaml
format: upc8
assignment_version: 0.2
canon_ref: ksetra/canon/siva-sutras.yaml@<sha>
profile: ukr-phonemic-v1
normalization: NFC
payload: <bytes>
```

Не обов’язково класти все це перед кожним byte array; достатньо зробити profile mandatory на frame/container boundary. Для hardware image можна мати compact profile ID, а manifest тримати поряд.

Також repository має кілька extension variants for Ukrainian and English without an explicit current authority, що вже зафіксовано consistency audit-ом [4]. UPC-8 не повинен мовчки hard-code-ити one variant. До вибору owner-ом authoritative registry best behaviour — reject ambiguous profile or require explicit `--registry` / profile version.

## 9. Епістемічний статус — не прикраса, а частина correctness

Власний audit repository коректно позначає UPC-8 як high-severity scope leak: README описує «encoding/hardware layer», але prototype не має `epistemic_layer`, `status` чи `hypothesis_ref`, хоча research manifesto і `hypotheses/shabda/status.yaml` ставлять UPC-8/FPGА work у `PREMATURE-HYPOTHESIS` [4] [7] [8].

Це не аргумент видалити prototype. Навпаки, його треба зберегти, бо він є valuable history of engineering thought і тестовим стендом. Але верхній header у README та code має містити приблизно таке:

```yaml
epistemic_layer: engineering
status: experimental
hypothesis_ref: hypotheses/shabda/status.yaml#H2
non_claims:
  - no historical claim about Panini's intended numeric encoding
  - no claim of universal phoneme inventory
  - no FPGA performance result
```

Цей marker зробить prototype сильнішим: він не відмовляється від амбіції, а точно каже, **який тип питання зараз тестується**.

## 10. Стан тестування

| Перевірка | Результат | Що вона доводить | Чого вона не доводить |
|---|---|---|---|
| Existing `test_upc8.py` | 20/20 PASS у локальному запуску | Internal code table, selected examples, no-gaps, alias metadata. | General pratyāhāra correctness; test encodes wrong `hal == 32` expectation. |
| Position-based pratyāhāra oracle | 301 API-valid forms; 81 mismatches | Systematic marker-token collision. | Full historical validity of every constructed two-token notation. |
| Input probes | IAST tokens and multi-token words fail as described above | Actual API is narrower than docs. | Correct final design for IAST/phonemic input. |
| Ukrainian probes | `джаз`, `льон` pass; iotated vowels fail | Present coverage boundary. | Correct language policy for Ukrainian. |
| CI inspection | No `.github` workflow directory found in clone | No discovered automatic run for suite. | That prototype can never be integrated into another external CI. |

Найважливіший test repair не в тому, щоб додати ще двадцять examples. Потрібен **property/reference test**: derive the result from typed positional source data, enumerate all API-accepted notation forms under declared marker resolution, then assert equality with engine output. Після minimal fix цей test має завершитися `301 checked, 0 mismatches` for the selected semantics.

## 11. Пріоритетний план, який не руйнує прототип

| Пріоритет | Крок | Очікуваний результат |
|---|---|---|
| **P0** | Add experimental/engineering/hypothesis header and rename ambiguous «canonical codes». | Епістемічно correct navigation для human та agent. |
| **P0** | Remove spelling-based marker skip; change `hal` expectation from 32 to 33; add six collision families to tests. | General pratyāhāra engine agrees with position model. |
| **P0** | Add exhaustive reference/property test. | Future refactors cannot silently reintroduce same class of error. |
| **P1** | Load/generate table from versioned authoritative data, or snapshot a manifest with source SHAs. | Data provenance and reproducibility. |
| **P1** | Split SLP1 token API, IAST token API and word tokenizer. | Documentation becomes true; language support can grow without ambiguity. |
| **P1** | Declare Ukrainian profile scope and add contextual decoder. | Clear distinction among graphemic, phonemic and transliterated modes. |
| **P2** | Define `canonical_class`, Sanskrit profile class and language-specific class APIs. | Extensions do not accidentally disappear from semantic queries. |
| **P2** | Generate bitmap tables and run separately versioned FPGA experiment. | A real engineering evidence record, not a prospective claim. |

## 12. Фінальний вердикт

UPC-8 має справжню цінність уже зараз, але вона не в тому, що він нібито відкрив «древній байтовий код». Його цінність у тому, що він виявив важливу architecture question: **як представити впорядкований фонологічний канон, мовні overlays, aliases, unresolved analysis та natural-class operations так, щоб жоден шар не видавав себе за інший?**

Прототип already демонструє хорошу відповідь на частину цього питання. Він поважає alias, не force-ить IPA certainty, відокремлює shared/new language units і передбачає multiple formats rather than forcing one byte value to serve every purpose. Але reliability поки що обмежена: general natural-class operation має відтворений bug, input contract треба звузити або реалізувати, а data/version/provenance треба зробити executable.

Тому правильний наступний крок — **не масштабувати UPC-8 до English/FPGA прямо зараз**. Спершу зробити маленьке ядро mathematically and contractually honest: typed positions/markers, 0 mismatch oracle, explicit profiles, version manifest і правильний experimental status. Після цього prototype стане чудовою основою для окремого, вимірюваного hardware experiment — без того, щоб змішувати інженерну зручність із claim-ом про самі Śiva Sūtras.

## References

[1]: https://github.com/juv4uk/shiva-sutras/blob/master/prototype/upc8.py "UPC-8 implementation"
[2]: https://github.com/juv4uk/shiva-sutras/blob/master/prototype/UPC8-documentation-ua.md "UPC-8 Ukrainian documentation"
[3]: https://github.com/juv4uk/shiva-sutras/blob/master/ksetra/canon/siva-sutras.yaml "Canonical Śiva Sūtras data"
[4]: https://github.com/juv4uk/shiva-sutras/blob/master/docs/EPISTEMIC_CONSISTENCY_AUDIT_v1.md "Epistemic consistency audit"
[5]: https://learnsanskrit.org/panini/shivasutras/ "The Shiva Sutras — Learn Sanskrit"
[6]: https://github.com/juv4uk/shiva-sutras/blob/master/prototype/test_upc8.py "UPC-8 test suite"
[7]: https://github.com/juv4uk/shiva-sutras/blob/master/hypotheses/shabda/status.yaml "Śabda hypothesis status"
[8]: https://github.com/juv4uk/shiva-sutras/blob/master/docs/research_manifesto.md "Research manifesto"
