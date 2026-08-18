# Що, крім фонем, життєво необхідно UPC: уроки основних 8-бітних кодувань

**Автор:** Manus AI  
**Дата:** 18 серпня 2026 року  
**Статус:** технічна рекомендація для UPC-8

## Коротка відповідь

Друже, **не варто витрачати UPC на копіювання старих ASCII-control characters**. `BEL`, `CR`, `LF`, `TAB`, `ENQ`, printer controls і подібне були потрібні телетайпам, терміналам та раннім лініям зв’язку, а не фонологічному формату.

Для UPC поза фонемами справді життєво необхідні не «службові символи для тексту», а чотири речі: **однозначне розширення**, **ідентичність і версія профілю**, **межа/довжина даних**, **строга поведінка при помилці**. Якщо UPC передає не лише isolated syllable, а повний матеріал для аналізу, потрібні також **явні лінгвістичні межі** та **канонічна нормалізація**.

> **Головний принцип:** UPC — не legacy text encoding, а binary representation protocol для фонологічних одиниць. Тому control layer має описувати граматику байтового потоку, provenance і безпечне майбутнє розширення, а не поведінку принтера.

## 1. Що історичні 8-бітні кодування насправді вчать

### ASCII: потрібні не всі control codes, а їхні ролі

ASCII початково був **7-bit** стандартом, який RFC 20 пропонував розміщувати у восьмибітному byte з нульовим high bit [1]. Він містив `NUL`, початки й кінці transmission, `CR`, `LF`, `ESC`, `SUB`, `CAN` і hierarchical information separators `FS`, `GS`, `RS`, `US` [1].

У ньому змішані чотири історично різні задачі: transport control, terminal/printer formatting, logical separators і code extension. Для UPC з них пережили час лише ідеї **extension**, **explicit structure**, **substitution/error policy** та **filler only under a known framing contract**.

| Ідея з ASCII | Чи брати в UPC? | Причина |
|---|---|---|
| `ESC`: префікс, що змінює читання наступних bytes | **Так, але у власному reserved range** | Це основа 2/3/4-byte extensions. |
| `FS/GS/RS/US`: ієрархічні межі | **Так, як семантику; не обов’язково як однобайтні legacy codes** | Корисні для word/morpheme/syllable/utterance boundaries. |
| `SUB` і `CAN` | **Так, як policy decoder-а** | Некоректний byte sequence не має непомітно стати фонемою. |
| `NUL` | **Лише як padding поза payload, якщо є explicit length** | Усередині UPC payload він не може мати магічний статус. |
| `CR`, `LF`, `TAB`, `BEL`, `FF`, device controls | **Ні** | Це presentation або obsolete device protocol, не фонологічна семантика. |
| `SO/SI`: stateful shift між таблицями | **Ні** | Stateful decoding збільшує ризик desynchronization; explicit extension cleaner. |

### ISO-8859, Windows-125x і KOI8: байт без явної угоди нічого не означає

ISO-8859 family зберіг ASCII lower half і додав локальні repertoires у single-byte table: `00–1F` controls, `20–7E` ASCII graphics, `80–9F` C1 controls, `A0–FF` additional graphics [2]. Але Windows-1252 заповнив більшість ISO C1 range `0x80–0x9F` друкованими символами на кшталт Euro sign, smart quotes, dashes та ellipsis [3].

KOI8-R так само зберігає ASCII lower half, але використовує верхні 128 positions для box drawing, математичних символів і Cyrillic; RFC 1489 описує його як de facto Cyrillic network encoding свого часу [4].

Висновок тут жорсткий: **не існує globally safe “службового байта” без письмового protocol agreement**. Один і той самий `0x80` може бути C1 control, Euro sign, box-drawing symbol або щось зовсім інше. Отже, UPC не має посилатися на «стандартне значення» ASCII/ISO byte; значення визначає тільки UPC grammar і його version.

### UTF-8: не копіюй таблицю, копіюй дисципліну

UTF-8 не є однобайтною code page, але він — найкращий lesson для твоєї ідеї 1/2/3/4-byte UPC. RFC 3629 робить first byte multi-byte sequence explicit length marker, забороняє частину byte values у валідному stream, дозволяє знайти character boundaries у byte stream і вимагає від decoder-ів reject invalid або overlong sequences [5].

Для UPC важлива саме ця дисципліна: **prefix tells length; one semantic unit has one canonical representation; impossible forms are rejected; a newer extension is not silently decoded as old core data.**

## 2. Критична особливість саме твого UPC-8

У поточному prototype уже зайняті `0x00–0x4F`: 42 Śiva Sūtras sounds, 7 Sanskrit extensions і 31 Ukrainian new units — разом 80 assigned values. Тому в payload **`0x00` не може раптом означати `NUL`, а `0x0A` не може означати `LF` лише через звичку операційної системи**. Це звичайні UPC code units, якщо саме так призначає твоя таблиця.

Саме через це raw UPC payload не слід трактувати як text, передавати C-string APIs або ділити на lines за `0x0A`. Для JSON, terminal display, git diff і log output потрібне окреме human-readable representation: hexadecimal (`UPC8: 00 17 …`), Base64 або explicit escaped notation. А binary UPC має йти як length-delimited bytes.

> **Наслідок:** не треба «повернути» ASCII controls у низькі values. Їх уже правильно займають фонемні units. Службовий простір треба виділити серед поки що вільних high values.

## 3. Мінімум, без якого UPC стане крихким

### 3.1. Однозначні extension prefixes — обов’язково

Твій direction `8-bit base + 2/3/4-byte extensions` правильний. Decoder мусить з першого byte знати, скільки bytes належать одному UPC unit. Це не cosmetic detail: без нього невідомий future code може бути хибно розібраний як декілька current phonemes.

Практичний стартовий partition, який **не ламає твої поточні assignments**, може бути таким:

| Byte range / lead | Значення у UPC v1 | Місткість |
|---|---|---:|
| `00–DF` | Direct base unit | 224 one-byte units |
| `E0 xx` | `EXT2`: один 16-bit extension identifier | 256 extension IDs |
| `E1 xx yy` | `EXT3`: один 24-bit extension identifier | 65,536 extension IDs |
| `E2 xx yy zz` | `EXT4`: один 32-bit extension identifier | 16,777,216 extension IDs |
| `E3–FF` | Reserved: only later, through a new grammar version | 29 lead values |

Тут у тебе залишається **144 direct values** після поточних 80 assignments. Але multi-byte capacity росте не на десятки, а на порядки. Важливіше, що grammar однозначна: `E1` завжди споживає exactly two payload bytes, незалежно від того, що вони означають.

```text
Direct:  3A
EXT2:    E0 91
EXT3:    E1 02 7F
EXT4:    E2 00 31 9C
```

`E0–E2` тут є **illustrative stable choices**, а не вимога. Важливий contract: whole range must be reserved before the first public data set, lead byte must determine total length, і direct assignments ніколи не повинні later invade this prefix space.

### 3.2. Version + assignment table + profile — обов’язково

Один UPC payload недостатній для research-grade interpretation. Потрібно знати:

| Metadata field | Навіщо він потрібен |
|---|---|
| `format_version` | Яку binary grammar застосовувати: ranges, extensions, validation rules. |
| `assignment_version` | Який stable UPC registry / table визначає code IDs. |
| `profile_id` + `profile_revision` | Яка language-specific mapping застосована: Sanskrit SLP1, Ukrainian, future English/Polish тощо. |
| `analysis_level` | Чи це orthographic mapping, broad phonemic form, narrow phonetic form, experimental analysis. |
| `normalization_id` | Які equivalent source forms зведено до canonical UPC representation. |
| `source_ref` або provenance ID | Звідки взявся profile або нетривіальне рішення. |

Це не обов’язково має стояти перед кожним словом. Але воно має бути в manifest, file header, database column або enclosing message. Без profile revision bytes можуть лишатися syntactically valid, але їхній зв’язок із конкретною мовною моделлю буде невідтворюваним.

### 3.3. Length-delimited frame — обов’язково для binary interchange

Не використовуй `NUL`, `EOF`, `LF` або «спеціальний final byte» як кінець UPC sequence. У потоці, де всі `00–DF` legal data, delimiter згодом конфліктуватиме або вимагатиме escaping.

Надійна модель — **container knows payload length**. Наприклад, це може бути file record, a packet, database blob or memory descriptor:

```text
UPC frame
  magic              "UPC"
  format_version     u8
  assignment_version u16
  profile_ref         variable / registry reference
  flags              u8
  payload_byte_len   unsigned integer
  payload            exactly payload_byte_len bytes
  integrity          optional CRC / hash, defined by container
```

`magic` допомагає не плутати UPC з arbitrary bytes, `payload_byte_len` забезпечує boundaries, а `integrity` має жити в container/transport layer. Це важливо і для FPGA: fixed-size memory cell може мати physical padding, але логічна довжина мусить бути окремим field. Тоді `0x00` у payload не «padding», а звичайна data unit.

### 3.4. Canonical validation and error contract — обов’язково

RFC 3629 прямо вимагає захисту від invalid sequences, бо невірний decoder може перетворити заборонені sequences на значущі characters [5]. Для UPC це ще критичніше: хибний extension не повинен перетворитися на іншу фонему і потім потрапити у linguistic inference.

UPC decoder варто зробити двохрежимним:

| Режим | Поведінка |
|---|---|
| **Strict** | Reject frame або payload із truncated extension, reserved lead, unknown assignment там, де known assignment required, чи non-canonical form. |
| **Forensic / permissive** | Повертає structured diagnostic: byte offset, raw bytes, grammar version і reason; не підміняє тихо на фонему. |

`SUB` був історичною ідеєю «поставити substitute замість invalid character» [1]. Для UPC краще, щоб заміна була **явним application-level decision**, а не тихою властивістю decoder-а. Якщо data каже «сегмент невідомий, але він існує», це можна представити окремим semantically defined `UNKNOWN_SEGMENT` extension. Якщо bytes physically corrupted, це має бути decoding error з provenance, а не той самий token.

### 3.5. Лінгвістичні boundaries — обов’язково лише коли потрібні семантиці

Фонемний stream без меж недостатній для many tasks. `/n a d i/` може бути достатнім для inventory counts, але недостатнім для morphophonology, sandhi, token-level round trip або навчальних derivations. Мінімально варто підтримати модель boundary annotations:

| Boundary kind | Коли потрібен | Рекомендоване місце |
|---|---|---|
| `WORD` | Tokenisation, text reconstruction, word-level rules | Inline annotation або enclosing token structure |
| `MORPHEME` | Paninian derivation, affixation, sandhi/provenance | Inline annotation або Derivation IR |
| `SYLLABLE` | Prosodic rules, metrics, phonotactics | Optional annotation layer |
| `UTTERANCE` / `PHRASE` | Prosody, speech corpus, phrase-level rules | Record/container layer |

Не треба зараз займати чотири bytes під fixed delimiters. Кращий шлях — зарезервувати один future extension namespace для **typed annotations**. Власне payload лишається компактним, а boundaries з’являються тоді, коли правило реально вимагає їх. Це добре узгоджується з твоїм підходом: будувати функції, коли вони стають потрібними.

## 4. Що не треба класти у UPC v1

| Річ | Чому не core UPC |
|---|---|
| Newline, tab, carriage return, form feed | Це display/text-formatting semantics. |
| Bell, terminal/device control, XON/XOFF | Це hardware/transport protocol semantics; у разі потреби належать UART or link layer. |
| Checksum / retransmission | Це frame/transport integrity, а не identity phonological unit. |
| Letter case, punctuation, typography | Це orthography/rendering. Для lossless original spelling потрібний окремий source layer або span mapping. |
| `NULL` as “unknown phoneme” | Missing data, unknown data і corrupted data — три різні стани; їх не можна сховати під одним byte. |
| Globally fixed language blocks | Profiles повинні reuse shared sound IDs, а не дублювати `/k/` окремо для кожної мови. |

## 5. Практичний UPC v1 contract

Я б зафіксував саме такий мінімум.

> **UPC v1 payload is a sequence of canonical UPC units. `00–DF` are direct units. `E0`, `E1`, and `E2` introduce exactly 2-, 3-, and 4-byte units respectively. All other lead bytes above `E2` are reserved and invalid in v1. Payload boundaries are supplied by an enclosing frame, never by NUL or a line terminator. The frame declares the grammar version, assignment-table version, profile revision, analysis level, and payload length. A strict decoder rejects malformed, truncated, reserved, and non-canonical sequences.**

Це дає тобі простий 8-bit fast path, зберігає всю твою поточну таблицю, і вже сьогодні прибирає головні design debts. Пізніше в reserved space можна додати annotation/unit modifiers, compression, vendor/research namespace або stronger self-synchronisation — але тільки як new, explicit grammar version.

## 6. Пріоритети: що зробити першим

| Пріоритет | Дія | Чому зараз |
|---|---|---|
| **P0** | Винести `UPCFormatVersion`, `AssignmentVersion`, `ProfileId`, `ProfileRevision`, `AnalysisLevel` у manifest/frame contract. | Без цього ранні mappings не мають відтворюваної ідентичності. |
| **P0** | Зарезервувати high prefix space й задокументувати grammar 1/2/3/4-byte units. | Це не дає майбутнім direct assignments зламати extensions. |
| **P0** | Визначити strict decoder errors і canonical encoding tests. | Потрібно, аби corruption або future bytes не стали false phonemes. |
| **P1** | Додати length-delimited binary frame та optional integrity hook. | Вирішує NUL/padding/stream boundaries без legacy hacks. |
| **P1** | Описати typed boundary annotation namespace. | Потрібне для Panini/derivation та morphology, але не треба впроваджувати все негайно. |
| **P2** | Text-safe exchange notation (`upc8:` hex/Base64) і test vectors. | Важливо для tools, documentation, diffs та FFI. |

## Висновок

Старі 8-bit encodings дають простий урок: **набір 256 positions майже ніколи не був головною проблемою. Проблемою були unstated assumptions — про table, language, byte boundary, error handling і future compatibility.**

Для UPC не потрібно відтворювати ASCII як музей. Потрібно взяти з нього `ESC`, separators і error awareness; з ISO/KOI8 — розуміння, що local mapping без profile неоднозначний; з UTF-8 — deterministic prefixes, validation, canonicality та evolution without reinterpretation.

Твоя модель виглядає здорово саме так:

```text
stable 8-bit phoneme core
  + reserved deterministic 2/3/4-byte extensions
  + immutable assignment versions
  + source-aware language profiles
  + explicit frame length and integrity boundary
  + optional typed linguistic annotations
  + strict decoding, never silent phoneme substitution
```

Це вже не просто таблиця фонем. Це компактний, hardware-friendly і epistemically honest interchange contract.

## References

[1]: https://www.rfc-editor.org/rfc/rfc20.html "RFC 20: ASCII format for Network Interchange"
[2]: https://www.ibm.com/docs/ssw_aix_72/globalization/iso8859_family.html "IBM: ISO8859 family"
[3]: https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WINDOWS/CP1252.TXT "Unicode mapping: Windows CP1252 to Unicode"
[4]: https://datatracker.ietf.org/doc/html/rfc1489 "RFC 1489: Registration of a Cyrillic Character Set (KOI8-R)"
[5]: https://datatracker.ietf.org/doc/html/rfc3629 "RFC 3629: UTF-8, a transformation format of ISO 10646"
