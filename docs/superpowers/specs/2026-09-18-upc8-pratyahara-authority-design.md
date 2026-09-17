# UPC-8 Pratyāhāra Authority — дизайн

**Дата:** 2026-09-18  
**Статус:** first slice implemented in PR #8  
**Гілка:** `chatgpt/upc8-pratyahara-authority`

## Мета

Звести канон Śiva Sūtras, механіку pratyāhāra та UPC-ознаки в один перевірюваний вертикальний зріз без дублювання канону й без ручних таблиць, що можуть розійтися між Python/Lisp/C/RTL.

## Джерело істини

`ksetra/canon/siva-sutras.yaml` лишається незмінним authority. Він уже правильно розділяє `sounds`, `it_marker_iast` і `text_iast`. Жоден похідний шар не має права перетворювати `it_marker_iast` на UPC sound code лише через збіг написання з реальною фонемою.

## Архітектура

### Canonical pratyāhāra expansion

Поточний slice повторно використовує наявні `load_sutras()`, `flat_sequence()` та `build_pratyaharas()` у `prototype/upc8_pratyahara_probe/probe.py`. Дані канону читаються безпосередньо з YAML; другої копії 14 сутр не створюємо.

Поточний probe формує ключ як literal `start sound + it-marker`, тому executable keys у цьому slice — `ñm`, `jś`, `hl`. Display/transliteration forms на кшталт `ñam` чи `jaś` не підміняють machine key.

### UPC predicate view

Окремий шар описує інженерний предикат над уже наявним `SA_FEATURES`. Predicate не є канонічним визначенням pratyāhāra; це незалежна машинна гіпотеза про те, чи можна ту саму множину отримати через feature geometry.

Перший slice містить:

```text
nasal     := manner == 3
consonant := manner != 5
```

`voiced-unaspirated-stop` навмисно не має selector: `SA_FEATURES` не містить aspiration, тому plain/aspirated voiced stops не можна чесно розділити одним поточним предикатом.

### Exactness classifier

Для перевірки обчислюємо:

```text
P = canonical expansion from Śiva Sūtras
U = UPC predicate expansion
```

Статуси:

- `EXACT` — множини однакові;
- `PARTIAL` — множини різні, але predicate обчислюваний;
- `NOT_SINGLE_PREDICATE` — поточний feature space не має потрібного виміру;
- `AMBIGUOUS_CANONICAL_SELECTOR` — зарезервовано для наступного occurrence-aware canonical API; у цьому slice не фабрикується.

Canonical membership перед порівнянням нормалізується до унікальних звуків у порядку першого входження. Це необхідно для `hl`: переданий канон має `h` у sūtra 5 і повторне `h` у sūtra 14, але class membership містить один `h`.

## Підтверджені witnesses цього slice

```text
ñm  ↔ nasal      => EXACT
     ñ m ṅ ṇ n

hl  ↔ consonant  => EXACT
     33 unique consonants; duplicate canonical h collapsed

jś  ↔ voiced-unaspirated-stop
     => NOT_SINGLE_PREDICATE
     reason: no aspiration dimension in SA_FEATURES
```

Це інженерні результати конкретного прототипу. `EXACT` не є історичною тезою про те, що Паніні використовував бітові маски.

## Взаємодія з наявними прототипами

- `prototype/upc8_pratyahara_probe/probe.py` лишається дослідницьким probe; nearest-neighbour metric не стає authority.
- `prototype/CANONICAL_PRATYAHARA_ORACLE_PASS1.md` використовується як аудит/підказка, але не як machine-readable source of truth.
- `prototype/upc8.py`, `bitmask64`, `cml_lowering`, `lisp_core_phonetics` та `fpga_alu` не отримують нових hand-maintained pratyāhāra tables.
- Майбутні C/Lisp/RTL masks мають генеруватися тільки після стабілізації occurrence-aware canonical result.

## Координація з активними задачами

- issue #3 (`ECO-LISP-SCRIPTS-1`): цей PR розширює вже існуючий Python probe, але не створює нового Python authority або нової membership table; майбутній стабільний consumer має узгодитися з Lisp-migration.
- issue #4: human-facing документація лишається українською; IAST/Pāṇinian terms і semantic IDs не перекладаються.
- issue #5: цей spec/plan мають бути враховані під час documentation-authority cleanup.

## Інваріанти

1. `ksetra/canon/siva-sutras.yaml` не змінюється.
2. `IT_MARKER` не отримує sound membership через spelling collision.
3. Canonical expansion і UPC predicate будуються незалежно.
4. `EXACT` вимагає рівності множин в обидва боки.
5. Case-sensitive identifiers не case-foldяться.
6. Generated mask/predicate не стає authority.
7. Відсутня feature dimension дає явний негативний результат, а не спеціальний lookup.

## Verification boundary

Локальний isolated-replica run:

```text
python -m pytest prototype/upc8_pratyahara_probe/test_compare.py -q
3 passed

python -m py_compile prototype/upc8_pratyahara_probe/probe.py \
  prototype/upc8_pratyahara_probe/test_compare.py
exit 0
```

У репозиторії немає загального Python CI workflow, тому цей PR не заявляє repository-wide CI green.

## Наступний slice

Occurrence-aware canonical selector для повторних it-marker spellings. Лише після цього варто генерувати спільний machine-readable result для Lisp/C/RTL і перевіряти ширший набір pratyāhāra.