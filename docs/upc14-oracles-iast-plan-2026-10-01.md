# План перетранслітерації оракулів UPC-14 з SLP1 в IAST (агент «шіва», 2026-10-01)

Статус: **план**, нічого не змінено в `prototype/`. Рішення власника (через координатора, 2026-10-01): SLP1 і великі літери з лабораторії UPC-14 прибрано; письмо = IAST (малі літери з діакритикою) і Деванагарі; ідентичність = код. Виконувати має власник зони `prototype/` (координатор); тут лише план і перевірки.

## Що запускав / читав / не перевірив

- Запускав: `git ls-tree`, `sha256sum`, `git grep` по `origin/master` `d194378`/`d54de8a`; нічого з перетворень не виконував.
- Читав: заголовки 4 TSV, код, що їх читає.
- Не перевірив: чи є інші споживачі цих TSV поза `prototype/` (`git grep` по `prototype/*.py` показав лише нижче перелічених).

## 1. Інвентар (стан `origin/master`)

| Файл | Рядків | sha256 (12) | Колонки (SLP1) | Походження |
|---|---|---|---|---|
| `prototype/oracles/ashtadhyayi-com-pratyahara.tsv` | 50 | 93ff2c3d0a44 | `name_devanagari`, `start_slp1`, `marker_slp1`, `sounds_slp1` | `ashtadhyayi-com/data` `pratyahara/data.txt`, коміт 5744762f; ліцензії нема: лише факти (назва й набір звуків) |
| `prototype/oracles/vidyut-sandhi-final-stops.tsv` | 104 | 640da4227ec9 | `first_slp1`, `second_slp1`, `result_slp1` | vidyut (MIT), `generator.rs`, коміт 8da2f90b |
| `prototype/oracles/vidyut-sandhi-vowels.tsv` | 159 | fa5a33d83033 | `first_slp1`, `second_slp1`, `result_slp1` | vidyut (MIT), той самий коміт; результат: пробіл між лівою і правою частиною, `'` = avagraha |
| `prototype/oracles/paninian-verified-consonant-maps.tsv` | 37 | 16b1b63e3d60 | `rule`, `coq_definition`, `input_slp1`, `output_slp1` | paninian-verified (MIT), `paninian.v`, коміт 9d2e3efa; Coq не запускали |

Споживачі: `test_upc14v2_oracles.py` (ashtadhyayi-com), `test_upc14v2_sandhi.py` (рядки 94, 115: `first_slp1`, `second_slp1`, `result_slp1`, `input_slp1`, `output_slp1`), `test_upc14v2_vowel_sandhi.py` (рядки 109-124). Окремо: `test_upc14v2.py` (рядки 41-44) читає `text_slp1` і `it_marker_slp1` з `ksetra/canon/siva-sutras-encoded.yaml`, тобто ще одне джерело SLP1; незмінний канон `ksetra/canon/siva-sutras.yaml` уже IAST (його використовує мій `tests/test_pratyahara_usage_canon.py`).

## 2. Відображення SLP1 → IAST (один символ SLP1 = один звук, без втрат)

`A→ā I→ī U→ū f→ṛ F→ṝ x→ḷ E→ai O→au K→kh G→gh N→ṅ C→ch J→jh Y→ñ w→ṭ W→ṭh q→ḍ Q→ḍh R→ṇ T→th D→dh P→ph B→bh S→ś z→ṣ M→ṃ H→ḥ`; решта (a i u e o k g c j t d n p b m y r l v s h) без змін. `X` (довге ḷ) у даних не зустрічається (Kāśikā txt 389: довгого ḷ нема); якщо з'явиться, помилка, не мовчазна заміна.

## 3. Формат клітинки (щоб не втратити однозначність)

IAST **неоднозначний при склеюванні**: `kh` проти `k`+`h`, `ai`/`au` проти `a`+`i`/`u`, `ṭh`, `jh` тощо. Тому послідовність звуків пишемо **токенами через пробіл**: `a i u` (набір), а в результатах sandhi ліву й праву частини розділяємо `|` (замість пробілу): `d | a`. Токени NFC-нормалізовані (`ṛ` = U+1E5B, `ṝ` = U+1E5D, `ḷ` = U+1E37).

## 4. Кроки

1. Скрипт `prototype/oracles/to_iast.py` (зона координатора): читає SLP1-TSV, відображає за таблицею §2, пише IAST-TSV; колонки `…_slp1` → `…_iast` (`start`, `marker`, `sounds`, `first`, `second`, `result`, `input`, `output`).
2. Один раз перед видаленням: зворотне відображення IAST→SLP1 мусить відтворити оригінал побайтово (round-trip), кількість рядків збігається.
3. Заголовок кожного TSV: «Transliterated from SLP1 to IAST by `prototype/oracles/to_iast.py`; original file at commit `<хеш коміту до зміни>`, sha256 `<з §1>`»; атрибуція upstream (MIT / лише факти) лишається як є.
4. Оригінальні SLP1-файли видаляються з дерева (історія git їх зберігає в зазначеному коміті).
5. Оновити читачів: назви колонок у трьох `test_upc14v2_*.py`; `test_upc14v2.py` перевести на `siva-sutras.yaml` (IAST), мітки `core/sandhi` на IAST (етап 2 координатора).
6. Прогнати тести: очікування те саме (13 + 26 + 22 + 29 OK на master; 97 з 99 і 127 з 154 + 27).

## 5. Ліцензія й провенанс

Дані `ashtadhyayi-com` без ліцензії: у TSV лише факти (назва, набір звуків); це не змінюється. vidyut і paninian-verified (MIT): збереження атрибуції в заголовку. Транслітерація не додає нового змісту.

## 6. Ризики

- Склеювання IAST у рядках (sandhi-результат як один рядок): розв'язано токенами (§3); тести, що порівнюють склеєні рядки (`.text`, `mine == theirs`), треба перевести на списки токенів.
- Комбінування діакритик: без NFC `ṛ` може бути двома кодпоінтами; тест на нормалізацію.
- `'` (avagraha) у vidyut-результатах: у IAST писати `’` або `ऽ`; пропозиція: `’` в IAST-колонці, `ऽ` у Деванагарі.
