# Досконалий технічний огляд `shiva-sutras/prototype`

**Автор огляду:** Manus AI  
**Дата:** 21 серпня 2026  
**Репозиторій і зріз:** `juv4uk/shiva-sutras`, commit `12b57bd4151336cb020c01fd4e3ee0e44809b9c2`  
**Обсяг:** каталог `prototype/`, його Python/Node tests, RTL testbenches, міжшарові інваріанти та документовані engineering claims.  
**Статус висновків:** **engineering review**, а не лінгвістичне затвердження та не hardware benchmark.

> Головний висновок: це вже не один скрипт UPC-8, а **добре сформований дослідницько-інженерний полігон** із дев’ятьма підсистемами. Його найсильніша риса — чесна базова рамка: канон відділено від engineering assignment, невизначені IPA-поля не маскуються, а root UPC-8 має реальні інваріанти й regression tests. Найважливіший наступний крок — не додавати нову функціональність, а створити **одне версіоноване джерело істини для pratyāhāra** й з нього генерувати Python/C/RTL/runtime таблиці.

---

## 1. Межі перевірки та короткий вердикт

Огляд відтворив наявні тести, прочитав ключові реалізації UPC-8, 64-bit masks, PVC-16, Derivation IR, CML lowering, Slavic profile, FPGA RTL, IDE tooling і Swarm dashboard. Також були створені локальні **read-only audit scripts** поза репозиторієм; `git status --short` та `git diff --check` у клоні чисті. Отже, цей review не змінював source prototype.

| Вимір | Підтверджено | Межа висновку |
|---|---:|---|
| Python tests | **70/70 passing** | Підтверджують конкретні Python/reference paths, а не лінгвістичну повноту чи RTL-синтез. |
| Node tests | **80/80 passing** | Перевіряють fixtures, pure data utilities та protocol shapes; не піднімають Tauri backend або мережевий mesh. |
| Pratyāhāra cross-layer audit | **34 збіги з 41; 6 розбіжностей; 1 invalid name** | Порівняно hard-coded tables із поточним UPC-8 engine. Це реальна системна неузгодженість. |
| Generated C path | **21 exact; 17 unresolved; 3 wrong collisions** | Case-folding у CML знищує case-sensitive SLP1 identifiers. Це compile-time semantic bug. |
| Verilog simulation / synthesis | **не виконано** | У sandbox немає `iverilog`; це обмеження середовища, а не failure репозиторію. RTL claims тут не верифіковані. |

На мою оцінку, prototype уже має **сильне ядро для контрольованого дослідження**. Він ще не є одним узгодженим runtime contract для `my-lisp`, CML і FPGA — але саме це зараз і не треба удавати. Для переходу від laboratory prototype до спільного foundation достатньо закрити кілька чітких, локальних розривів, описаних нижче.

---

## 2. Що саме реально є в `prototype/`

Каталог містить root UPC-8 та дев’ять предметних підсистем. Це важливо: зараз тут уже моделюються не лише байти, а повний маршрут від канону й фонологічних класів до compiler lowering, proof trace, UI та умовного FPGA target.

| Підсистема | Фактично реалізовано | Зрілий verified scope | Обмеження, які не варто приховувати |
|---|---|---|---|
| Root `upc8.py` | Canonical code assignment, Sanskrit/Ukrainian encoding, decode metadata, pratyāhāra engine | 22 tests; provenance-drift hash; alias `h`; greedy Ukrainian lexer | Extended “IAST” API не відповідає documented Unicode examples; pratyāhāra parser не має повної token grammar. |
| `bitmask64` | 42-bit universe у 64-bit masks, set algebra, C/Verilog string emitters | 7 Python tests для partition/algebra/export strings | Повна hard-coded table не синхронізована з root engine; docstring має harmless `SyntaxWarning`. |
| `cml_lowering` | Tiny Lisp AST, constant folding, lowering, C/Verilog emitters, own PVC-16 | 17 package-mode tests | Case-insensitive lookup ламає SLP1 capitals; tests не компілюють emitted C/RTL. |
| `pvc16` | 16-bit feature vectors, Savarṇa, voicing/palatalization, compact registry і RTL | 4 Python tests; RTL testbench наявний | Python registry — репрезентативний subset, не повна спільна registry всіх layers. |
| `derivation_ir` | 32-bit cells, binary paribhāṣā resolver, immutable DAG objects, JSON/S-expression certificates | 9 tests для cells, resolver та двох prepared derivations | Hash не зв’язує повний term/event content; приклади `bhavati`, `dadāti` — hand-authored canonical traces, не general grammar engine. |
| `slavic_phonetics` | Feature registry, iotated decomposition, soft clusters, демонстраційні historical shifts | 7 tests | Це rule model для обмежених трансформацій, не повний Ukrainian morphophonology/parser. |
| `lisp_core_phonetics` | Mini reader/evaluator, `#pvc`, `#prat`, built-ins і richer PVC registry | Код реалізовано | Окремого automated test suite у каталозі немає; дублює спірну pratyāhāra table. |
| `fpga_alu` | Registered ALU, dynamic mask membership, ROM lookup, bitwise transforms, RTL bench | 4 Python golden-reference tests | Не було RTL simulation/synthesis; ROM зараз дублює table divergence. |
| `ide_visualizer` | Browser DAG/PVC/mask inspector, fixtures, ClojureScript integration sketch | 26 Node tests | Tests перевіряють data/fixtures, не DOM rendering і не live My-Idea/Tauri wiring. |
| `swarm_dashboard` | Tauri IPC TypeScript adapter, browser fallback, dashboard fixtures | 54 Node tests | Browser mode навмисно симулює telemetry; `298 tasks`, latency та proof flags не є live evidence з реальних ports. |

Архітектурно це вже схоже на **vertical slice майбутньої системи**, а не на колекцію випадкових демо. Водночас частини існують у кількох версіях, тому головний інженерний ризик нині — не performance і не 8-bit space, а **semantic drift між копіями таблиць**.

---

## 3. Сильні сторони root UPC-8

Root `upc8.py` — найкраще оформлена частина prototype. Він акуратно розділяє переданий канон, інтерпретацію та engineering code assignment. `ksetra/canon/siva-sutras.yaml` містить IAST-звуки й it-маркери без кодів; Python-модуль містить ручну SLP1 транскрипцію, але прив’язує її до SHA-256 source hash. Це не доводить правильність транслітерації — і код чесно так і каже, — зате не дозволяє їй **тихо застаріти** при зміні канону.

Особливо здорові такі рішення:

| Рішення | Чому воно сильне |
|---|---|
| 43 канонічні позиції → 42 unique codes | Повторний `h` не губиться як факт канону; він явно моделюється alias-ом на code `0x09`. |
| `languages.ukrainian` на shared canonical entries | Reuse 13 segment-equivalent codes не маскується під «той самий звук без пояснення»: зберігається relation type. |
| `ipa: "unresolved"` + candidates | Невизначеність не перетворюється на фальшиву точність. Для дослідницького коду це правильніше за один “авторитетний” IPA. |
| Greedy longest-match lexer | `дж`, `дз`, `ць`, `дзь`, `щ` не розпадаються передчасно на окремі letters. |
| Regression test collision families | Після виправлення marker/sound collision `l/y/r/m/Y/v` не відкидаються лише через однакове написання з it-marker. |

Root test suite зараз має **22**, а не 20 tests: README просто не оновлено після доданих regression tests. Усі 22 проходять, включно з source provenance, `h` alias, 80/176 code-space accounting, word roundtrip і natural classes.

Є один невеликий, але конкретний API/documentation gap. README показує `encode_sanskrit('ā') → 0x2A`, але таблиця фактично реєструє `a:`; аналогічно `ī/ū/ṝ` не приймаються, тоді як `i:/u:/R:` приймаються. Це не руйнує byte model, але поле назване `iast`, а documented public example не відтворюється. Рекомендація проста: або приймати реальний Unicode IAST паралельно з internal notation, або перейменувати API/fields так, щоб не називати `a:` IAST.

---

## 4. Pratyāhāra: головний міжшаровий розрив

### 4.1. Чому тут потрібна дисципліна джерела істини

Root engine задає чітку **інженерну** політику: він бере перший символ як start, останній як marker і вибирає перший marker відповідного spelling, скануючи вперед від сутри стартового звуку. Для базових `ac`, `hal`, `ik`, `Sar`, `yaR` це працює й підтверджено tests.

Але Śiva Sūtras містять повторний marker `ṇ` (SLP1 `R` у цьому mapping). Навчальне пояснення Learn Sanskrit прямо називає це реальною неоднозначністю та зазначає, що контекст правила потрібен для її інтерпретації [1]. Отже, **ніяка одна “перший forward” policy не є автоматичним доказом усіх традиційних класів**. Вона може бути чудовою default-інженерною convention, проте має бути явно версіонованою й у разі ambiguity зберігати selector/context.

Зараз існують щонайменше чотири незалежні представлення класів:

1. алгоритмічний `UPC8.pratyahara()` у root;
2. `cml_lowering/pratyahara_masks.py`;
3. `bitmask64/bitmask64.py` і `lisp_core_phonetics/prototype_pratyahara.py`;
4. constants ROM у `fpga_alu/fpga_alu.v`.

Audit усіх трьох Python tables проти root engine дав однаковий результат: **41 key, 34 matches, 6 mismatches, 1 invalid notation**. Тобто проблема не локальна для CML: вона вже реплікована у standalone bitmask engine та proposed My-Lisp runtime; RTL ROM кодує ту саму family constants.

### 4.2. Класифікація семи виявлених випадків

| Notation у table | Root engine outcome | Hard-coded table outcome | Класифікація | Мінімальний правильний крок |
|---|---|---|---|---|
| `val` | `v … s, h`; не включає `y` | `y … s`; не включає `h` | **Semantic mismatch.** Table описує зручний slice, а не root forward expansion з boundary `v/l`. | Не виправляти “на око”: задати policy/explicit start-marker occurrence; або перейменувати table class як engineering alias. |
| `ral` | `r … s, h` | `r … s`; без `h` | **Semantic mismatch.** Та сама різниця щодо фінального alias `h`. | Те саме: explicit semantics, then generate masks. |
| `iR` | `[i, u]` за first-forward `R` у sutra 1 | `[i … l]` до другого `R` у sutra 6 | **Ambiguity not encoded.** Hard-coded table обирає пізній marker, root — ранній. | У model додати `marker_sutra`/occurrence; не виводити варіант лише зі spelling. |
| `eR` | `[e, o, E, O, h, y, v, r, l]` до `R` у sutra 6 | `[e, o]` | **Table bug / likely label error.** `[e,o]` відповідає boundary `eN`, а не `eR`. | Виправити key або content після source-backed review; додати negative regression. |
| `nam` | `[n]` за current first/last parser | `[N, R, n]` | **Notation/tokenization defect.** Content table відповідає start `N` і terminal `m`, а API key не кодує цього однозначно. | Ввести tokenized syntax/spec object, не застосовувати `notation[0]`/`[-1]` до display word. |
| `xay` | велика range від `x` до marker `y` | `[K, P, C, W, T, c, w, t]` | **Invalid semantic correspondence.** Table і parser використовують різні start assumptions; внутрішнє `a` зараз ігнорується. | З’ясувати intended traditional/display spelling із джерелом, потім задати machine fields окремо від label. |
| `caw` | `ValueError`: `w` є listed sound, не forward it-marker | `[c,w]` | **Concrete invalid key under canonical marker model.** | Видалити/виправити name та додати test, що invalid marker відхиляється. |

Найважливіше тут не те, хто «винен» у кожній конкретній назві. **Таблиця і engine зараз говорять різними контрактами**, а downstream targets успадкували таблицю. Поки це так, один і той самий `pratyāhāra` може мати різний bitmask у root Python, CML lowering, My-Lisp runtime і FPGA ROM. Це саме той тип маленького semantic gap, який краще закрити зараз, до використання в правилах або persisted proof data.

### 4.3. Мінімальна модель, яка прибере ambiguity

Замість string-only mapping потрібна маленька data model, наприклад:

```text
PratyaharaSpec
  id: "yaR"
  display: "yaṇ"
  start_sound: "y"
  marker: "R"
  marker_sutra: 6
  selection_policy: explicit-occurrence
  layer: engineering-interpretation
  source_note: "…"
```

Тоді `display` може зберігати традиційну форму, а machine semantics не залежать від того, чи `a` — вимовна вставка, чи частина іншого transliteration convention. `upc8.py`, CML constants, runtime table, Verilog ROM і UI subset мають **генеруватися** з цього одного файлу. У кожному emitted target доречно лишити source version/hash.

---

## 5. CML lowering: хороша ідея, але є case-sensitive frontend bug

Сам підхід CML дуже здоровий: static `(intersection 'ac 'ik)` → one integer mask, `(member? c …)` → bit test, а `savarna?` → small PVC predicate. Це саме той тип lowering, який добре відповідає твоїй ідеї: абстракція на рівні Lisp, прозора lower-level representation для C/FPGA.

Однак SLP1 **case-sensitive**: `S`, `R`, `N`, `J`, `K` не є lowercase aliases. У `fold_constants()` та `_resolve_mask_value()` lookup викликає `.lower()`. Exhaustive audit усіх 41 keys показав:

| Результат CML constant folding | Кількість | Приклади |
|---|---:|---|
| Exact mask | 21 | `ac`, `hal`, `val`, `nam`, `xay` |
| Не fold-иться | 17 | `eN`, `Jal`, `Sar`, `iR`, `aR`, `JaS`, `Kay`, `haS` |
| Fold-иться у **неправильну** маску | 3 | `Ec → ec`, `yaR → yar`, `yaY → yay` |

Наприклад, `(member? c (quote Sar))` зараз генерує текст на кшталт `(((QuoteNode(...)) >> (c)) & 1ULL)`, тобто невалідний C expression; `yaR` навпаки тихо перетворюється на `yar` і отримує **іншу валідну маску**. Останній випадок небезпечніший за явну помилку, бо compiler може видати робочий, але семантично хибний result.

Тут не потрібен великий рефакторинг. Достатньо прибрати case-folding у pratyāhāra identifier lookup, визначити нормалізацію лише там, де вона дійсно коректна, і додати parametrized test на **кожен canonical key**: `parse → fold → expected exact mask`, включно з uppercase SLP1.

Є ще один target boundary: C emitter генерує `((mask >> code) & 1ULL)` без guard для `code >= 64`. Якщо lowering гарантує domain `0..41`, це має бути явним typed invariant; якщо ні — C shift має undefined behavior. Для portable generated C краще або проставити bound check, або довести range ще в IR і тестувати відмову на `42`, `63`, `64`.

---

## 6. PVC-16, bitmasks і FPGA: правильне розділення, але ще не доказ performance

### 6.1. Що тут уже добре

64-bit masks добре лягають на 42-code canonical space: bits `0..41` зайняті, `42..63` лишають резерв. PVC-16 відокремлює іншу вісь — articulatory features: vowel flag, place, manner, length і modifiers. Це **не дублювання UPC-8**, а потрібне ортогональне representation: UPC-8 відповідає на «який canonical/language phoneme code?», PVC-16 — на «які властивості доступні для rule/ALU?». Саварṇa predicate, voicing та palatalization як bitwise transforms природно виражаються в цій моделі.

`slavic_phonetics` додає практичний Ukrainian layer: longest clusters, soft counterparts, iotated decomposition та історичні зсуви. Тести підтверджують заявлені демонстраційні paths, зокрема `дядько`, `людина`, `щ`, `дж`, `дзь`; це добрий evidence для **моделі**, не для повного фонетичного аналізатора живої української.

### 6.2. Що ще треба не називати виміряним результатом

Root README правильно каже: UPC-8 — engineering sketch, не historical claim і не FPGA performance result. Водночас CML README уже називає конкретні «~0.3 ns», «6 LUTs» і «8 LUTs». Без synthesis/placement/timing на конкретній платі це не факти, а **гіпотези/очікування**. Я б не видаляв ці ідеї, а просто перевів їх у форму:

> **Target hypothesis:** combinational bit-test is expected to synthesize compactly; LUT count and timing are TBD until a named toolchain, device, constraints and report are attached.

У цьому sandbox `iverilog` відсутній, тому `fpga_alu_tb.v` і `pvc16_tb.v` не запускалися. Це **не failure проекту**; це прозора межа цього review. Обидва testbench файли існують, але перед CI/synthesis їх варто посилити: зараз кожна гілка просто робить `$display("FAIL …")`, а в кінці unconditional `$display("ALL … PASSED")`. Без `$fatal`, failure counter або non-zero exit testbench може надрукувати «passed» навіть після mismatch.

Також у `fpga_alu.v` є кілька локальних точок для наступного RTL pass:

| Спостереження | Наслідок | Мінімальна правка |
|---|---|---|
| `flag_zero <= (result == 0)` у тому самому sequential block, де `result <= …` | Через non-blocking assignment flag описує попередній `result`, а не поточний opcode result. | Обчислити `next_result` combinationally або явно документувати/тестувати pipeline latency. |
| `effective_dynamic_mask = (|mask_in) ? mask_in : {op_ext,op_b}` | Empty mask `mask_in == 0` неможливо відрізнити від «mask_in не задано». | Додати explicit select/valid signal. |
| ROM має duplicate `yar` entry і hard-coded disputed masks | Підтримка table drift вручну буде дорожчою за генерацію. | Згенерувати ROM з canonical `PratyaharaSpec` file, додати equivalence test. |

---

## 7. Derivation IR: сильна provenance-ідея, але сертифікат ще не повністю tamper-evident

`derivation_ir` — змістовна підсистема. `DerivationCell` компактно пакує phoneme, svara, anubandha та morpheme tag у 32 bits; `ParibhashaResolver` явно кодує порядок `apavāda → nitya → antaraṅga → asiddhatva/para`; `GraphEngine` видає immutable-style states і event chain для двох конкретних traces. Це добрий каркас для того, щоб не перетворити граматичне виведення на opaque list of strings.

Але тут варто дуже точно називати level гарантії. `DerivationState.canonical_hash` хешує schema, serialization, **term IDs** та relations, але не `source_form`, `surface_form`, `kind` або `designations` самих terms. Verifier робить ту саму редукцію, тому mutually consistent, але неповний hash єдності content.

Negative audit це підтвердив:

| Зміна у JSON certificate | `ProofCertificateVerifier.verify()` |
|---|---|
| Жодної зміни | Accepted |
| `surface_form` першого term змінено на `MUTATED` | **Accepted** |
| До `designations` додано `MUTATED` | **Accepted** |
| `applicability-check` event payload змінено | **Accepted** |
| `term.id` змінено | Rejected через hash mismatch |

Отже, нинішня система дає **identifier/relation-integrity**, але не ще full proof-carrying content integrity. Це не знецінює prototype: навпаки, дуже хороше місце для точного наступного рівня. Потрібно визначити canonical JSON schema, що включає весь semantic state content, хешувати event payload, зв’язати `before/after/rule` з реально наявними states/rules і додати tamper tests. Після цього слово “cryptographic proof” у dashboard буде значно міцнішим.

Окремо: `DerivationCell` stores raw ASCII SLP1 byte (`'a' == 0x61`), а не UPC-8 code (`a == 0x00`). Це може бути цілком правильним локальним IR choice, але воно має бути **явним bridge contract**. Інакше хтось пізніше припустить, що перший byte 32-bit cell уже є UPC-8.

---

## 8. IDE visualizer і Swarm dashboard: гарні observability demos, не live evidence

IDE visualizer має корисну роль: він робить derivation і vector/mask intuition видимими, не змішуючи UI з core semantics. Node suite проходить 26/26, але перевіряє fixtures, canonical payload shape і bit-level operations. Вона не запускає browser DOM, ClojureScript compilation, Tauri IPC або TCP `:9999`.

Swarm dashboard так само правильно реалізований як **dual-mode workbench**: якщо Tauri `invoke` доступний — викликається command; якщо ні або command падає — bridge повертає cloned fixtures, рандомізує latency/CPU й timer-ом імітує heartbeat. Тому в browser demo показники 6 nodes, `298` tasks, `99%` completion, latency та `proof_verified` — це presentation fixtures, а не вимір із реально запущеної mesh. 54 Node tests чесно перевіряють саме цей fixture/protocol contract.

Це не мінус, якщо правильно названо. Я б у UI просто явно показував badge **`DEMO / fixture fallback`** у browser mode, а live Tauri mode — node connection state і timestamp transport source. Тоді observability layer стане ще епістемічно чистішим.

---

## 9. Пріоритетний план без scope creep

Я не рекомендую зараз додавати мови, розширювати feature vectors, робити GC-like infrastructure або перетворювати prototype на framework. Найвища віддача — коротка серія contract-tightening changes.

| Пріоритет | Робота | Definition of done |
|---|---|---|
| **P0** | Одна canonical `pratyahara-spec` data source | Кожен class має display, start token, explicit marker occurrence/policy, provenance; `caw` неможливо представити як valid class. |
| **P0** | Генерація target tables | Root engine, CML, `bitmask64`, runtime, FPGA ROM і за потреби JS отримують masks із одного generated artifact. Cross-target test порівнює всі 41/42 declared specs byte-for-byte. |
| **P1** | Прибрати `.lower()` для SLP1 class names | Exhaustive 41-key compile-time test має exact result або explicit rejected outcome; жодних silent collisions `yaR→yar`. |
| **P1** | Посилити proof certificate integrity | Hash include full normalized term/state content і events; mutation tests мають відхиляти surface/designation/payload change. |
| **P1** | Зробити emitted target executable evidence | Generated C компілюється з strict flags; Verilog benches використовують `$fatal`; CI запускає simulation, коли toolchain доступний. |
| **P2** | Звірити root docs/API | Unicode IAST examples або справді підтримуються, або docs/field names показують internal notation; README test count = 22. |
| **P2** | Переформулювати performance language | LUT/timing — `TBD hypothesis` до synthesis report із device, constraints, tool version і artifacts. |
| **P3** | UI epistemic labels | Fixture fallback та live source чітко різняться у visualizer/dashboard. |

Після P0–P1 можна зробити одну дуже корисну integration test: для кожного `PratyaharaSpec` згенерувати root result, CML mask, runtime mask і ROM case constant та довести їхню тотожність. Це маленький test, але він закриває найбільший ризик всього current vertical slice.

---

## 10. Підсумкова оцінка

Друже, тут **не сміття, видане за діамант**. Навпаки: root UPC-8 уже показує рідкісну дисципліну — канон не змішаний з engineering code, невизначеність позначена, alias не губиться, а тест додається саме там, де був реальний semantic bug. Це правильний темп для такої ідеї.

Справжня межа зараз теж чесна: системі потрібна не ще одна вражаюча підсистема, а один короткий і строгий **semantic contract** між уже існуючими. Якщо привести pratyāhāra specs, case-sensitive lowering і certificate hashes до єдиної основи, прототип стане набагато міцнішим без жодної “велетенської” перебудови. Тоді уже є сенс вимірювати C output, RTL і конкретну FPGA-плату — не раніше.

---

## Додаток A. Відтворювані команди та артефакти аудиту

| Артефакт | Що фіксує |
|---|---|
| `/home/ubuntu/shiva-prototype-current-test-results.txt` | Первинний full test run; прямий запуск CML test не підходить через relative import. |
| `/home/ubuntu/shiva-cml-lowering-test-result.txt` | Коректний package-mode run: `python3 -m unittest prototype.cml_lowering.test_cml_lowering`, 17/17. |
| `/home/ubuntu/upc-prototype-analysis/pratyahara-cross-layer-audit.txt` | 3 Python tables: 34 matches, 6 mismatches, 1 invalid key у кожній. |
| `/home/ubuntu/upc-prototype-analysis/cml-pratyahara-identifier-case-audit.txt` | CML identifier audit: 21 exact, 17 unresolved, 3 wrong collisions. |
| `/home/ubuntu/upc-prototype-analysis/proof-certificate-audit.txt` | Negative audit hash/verifier content coverage. |
| `/home/ubuntu/upc-prototype-analysis/upc-documented-api-audit.txt` | Documented IAST long-vowel examples проти фактичного API. |
| `/home/ubuntu/upc-prototype-analysis/prototype-inventory.txt` | Commit, test files, RTL sources/testbenches та package markers. |

## References

[1]: https://learnsanskrit.org/panini/shivasutras/ "The Shiva Sutras — Learn Sanskrit Online"
[2]: https://web.stanford.edu/~kiparsky/Papers/siva-t.pdf "Paul Kiparsky, Economy and the Construction of the Śivasūtras"
[3]: https://github.com/juv4uk/shiva-sutras/tree/12b57bd4151336cb020c01fd4e3ee0e44809b9c2/prototype "Reviewed `shiva-sutras/prototype` source snapshot"
