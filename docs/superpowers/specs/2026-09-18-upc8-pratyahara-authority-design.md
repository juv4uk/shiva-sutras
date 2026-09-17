# UPC-8 Pratyāhāra Authority — дизайн

**Дата:** 2026-09-18  
**Статус:** design approved in conversation; implementation not started  
**Гілка:** `chatgpt/upc8-pratyahara-authority`

## Мета

Звести канон Śiva Sūtras, механіку pratyāhāra та UPC-ознаки в один перевірюваний вертикальний зріз без дублювання канону й без ручних таблиць, що можуть розійтися між Python/Lisp/C/RTL.

## Джерело істини

`ksetra/canon/siva-sutras.yaml` лишається незмінним authority. Він уже правильно розділяє:

- `sounds` — канонічні звукові елементи сутри;
- `it_marker_iast` — термінальний it-маркер;
- `text_iast` — переданий рядок для людини.

Жоден похідний шар не має права перетворювати `it_marker_iast` на UPC sound code лише через збіг написання з реальною фонемою.

## Архітектура

### 1. Canon adapter

Похідне представлення повинно давати типізовані елементи:

```text
SOUND(sound_iast, sutra_id, sound_index)
IT_MARKER(marker_iast, sutra_id)
```

Це представлення генерується тільки з `siva-sutras.yaml`; ручної другої копії 14 сутр не створюємо.

### 2. Canonical pratyāhāra expansion

Pratyāhāra визначається канонічною послідовністю і occurrence-aware terminal marker. Результат — впорядкована множина/послідовність `SOUND`, без `IT_MARKER` у membership.

Повторні marker spellings (`ṇ` та інші неоднозначності) не вирішуються case-folding або «першим рядком у таблиці». Selector/policy має бути явним і версіонованим там, де notation сама по собі неоднозначна.

### 3. UPC predicate view

Окремий шар описує інженерний предикат над UPC fields, наприклад:

```text
class == VOWEL
class in {VARGA, NON_VARGA}
manner == NASAL
manner == VOICED && aspirated == false
```

UPC predicate не є канонічним визначенням pratyāhāra. Це незалежна машинна гіпотеза про те, чи можна ту саму множину отримати через feature geometry.

### 4. Exactness classifier

Для кожної перевірюваної pratyāhāra обчислюємо:

```text
P = canonical expansion from Śiva Sūtras
U = UPC predicate expansion
```

і класифікуємо:

- `EXACT` — `P == U`;
- `PARTIAL` — є непорожній перетин, але множини різні;
- `NOT_SINGLE_PREDICATE` — немає чесного одного feature predicate без lookup/special cases;
- `AMBIGUOUS_CANONICAL_SELECTOR` — notation потребує явного selector/context до порівняння.

Заборонено «підправляти» canonical expansion, щоб вона збіглася з UPC predicate.

## Межі першої реалізації

Перший vertical slice охоплює тільки невеликий набір добре мотивованих класів:

- `ac`;
- `hal`;
- `jaś`;
- `ñaṇ`/відповідний nasal-class case тільки після occurrence-aware перевірки notation;
- `yaṇ` або інший semivowel class лише якщо canonical selector однозначний у поточному oracle.

Не намагаємося в першому PR класифікувати всі можливі pratyāhāra.

## Взаємодія з наявними прототипами

- `prototype/upc8_pratyahara_probe/probe.py` лишається дослідницьким probe; його nearest-neighbour metric не стає authority.
- `prototype/CANONICAL_PRATYAHARA_ORACLE_PASS1.md` використовується як аудит/підказка, але не як machine-readable source of truth.
- `prototype/upc8.py`, `bitmask64`, `cml_lowering`, `lisp_core_phonetics` та `fpga_alu` не отримують нових hand-maintained pratyāhāra tables.
- Майбутні C/Lisp/RTL masks мають генеруватися з одного machine-readable result після стабілізації цього зрізу.

## Координація з активними задачами

Робота не повинна конфліктувати з:

- issue #3 (`ECO-LISP-SCRIPTS-1`): не створюємо довгоживучий новий Python authority; якщо тестовий Python helper потрібен тимчасово, він має бути явно migration-target і не дублювати таблиці;
- issue #4: human-facing документація лишається українською; semantic IDs/IAST/терміни Паніні не перекладаємо;
- issue #5: новий design/spec є активним документом і має бути discoverable при майбутньому documentation-authority cleanup.

## Інваріанти

1. `ksetra/canon/siva-sutras.yaml` не змінюється.
2. `IT_MARKER` ніколи не отримує sound membership лише через spelling collision.
3. Canonical expansion і UPC predicate будуються незалежно.
4. Порівняння множин детерміноване й тестоване.
5. Case-sensitive IAST/SLP1 identifiers не case-foldяться.
6. Жоден generated mask не стає новим authority.
7. Невизначеність позначається явно, а не маскується «правильним» lookup value.

## Тестова стратегія

Мінімальний набір тестів має перевіряти:

- 14 сутр читаються з canon source без ручної копії;
- для кожної сутри `sounds` і `it_marker_iast` залишаються різними типами;
- marker/sound spelling collisions не викидають справжні sounds;
- canonical expansion відтворює відомі regression cases поточного root engine;
- `EXACT` вимагає рівності множин в обидва боки;
- навмисно неправильний UPC predicate класифікується `PARTIAL` або `NOT_SINGLE_PREDICATE`, а не `EXACT`;
- ambiguity не вирішується неявно.

## Критерій завершення першого зрізу

Перший зріз завершений, коли один executable test/report для вибраних pratyāhāra показує поруч:

```text
notation
canonical members
UPC predicate
UPC members
status: EXACT | PARTIAL | NOT_SINGLE_PREDICATE | AMBIGUOUS_CANONICAL_SELECTOR
```

і всі дані канону походять безпосередньо з `ksetra/canon/siva-sutras.yaml`.
