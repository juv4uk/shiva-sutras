# UPC-8 / Pratyāhāra Lisp migration — дизайн

**Дата:** 2026-09-18  
**Статус:** revised after owner correction: active repo-owned tooling moves from Python to my-lisp  
**Гілка:** `chatgpt/upc8-pratyahara-authority`

## Мета

Не створювати нового Python authority у `shiva-sutras`. Перший крок — повернути виправлену Lisp-копію phonetics knowledge base з `my-lisp`, додати нативний `.lisp` regression witness і використовувати Python лише як тимчасовий reference до differential parity згідно з issue #3 (`ECO-LISP-SCRIPTS-1`).

## Authority

- `ksetra/canon/siva-sutras.yaml` — immutable transmitted-canon authority; не редагується.
- `prototype/lisp_core_phonetics/prototype_phonetics.lisp` — engineering Lisp representation/masks, derived from canon; не замінює canon.
- Старі `.py` прототипи — reference/migration inputs, не новий шлях розвитку.

## Перший vertical slice

1. Backport corrected pratyāhāra masks із `juv4uk/my-lisp:prototype/lisp_core_phonetics/prototype_phonetics.lisp`.
2. Додати `prototype/lisp_core_phonetics/test_pratyahara_masks.lisp`.
3. Test script читає Lisp knowledge base через `read-file`/`read`, дістає `pratyahara-masks` через `assoc` і перевіряє точні значення `ac`, `hal`, `al`, `ik`, `ec`, `yar`, `Sar`, `JaS`, `Jal`.
4. При невідповідності test викликає навмисно незв'язаний `pratyahara-mask-regression-failed`, щоб процес завершився реальною помилкою; при успіху друкує `pratyahara-mask-regression-green`.
5. Новий Python comparison layer, створений помилково в цій гілці, видаляється. Існуючий старий Python probe лишається незмінним до окремого parity migration кроку.

## Чому не переносимо зараз весь `probe.py`

Issue #3 вимагає заміну active repo-owned Python із збереженням I/O/exit contract і differential parity. `probe.py` одночасно містить YAML parsing, pratyāhāra expansion, hand-curated feature space, metric і report formatting. Це окремий міграційний slice. Переписати все одним PR без parity gate означало б змішати мовну міграцію з research-semantic змінами.

## Інваріанти

1. Canon YAML не змінюється.
2. Нових Python-файлів/тестів у цьому slice немає.
3. Corrected masks у `shiva-sutras` мають збігатися з виправленою `my-lisp` reference-копією.
4. Lisp test не дублює алгоритм побудови pratyāhāra; він є regression witness для derived masks.
5. Наступний крок для `probe.py` — RED differential parity: Python output ↔ Lisp output на тих самих fixtures, потім переключення automation, потім видалення Python.

## Критерій завершення slice

- branch diff не містить нової Python production/test логіки;
- `prototype_phonetics.lisp` містить corrected masks;
- існує нативний `.lisp` regression script;
- script реально запускається на `my-lisp-cli` і дає green output перед merge.
