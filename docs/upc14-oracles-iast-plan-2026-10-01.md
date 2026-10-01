# План переходу оракулів UPC-14 з SLP1 на IAST (для читання) і Деванагарі (другий вид) (агент «шіва», 2026-10-01)

Статус: **план** (оновлено 2026-10-01 за уточненням власника), нічого не змінено в `prototype/`. Рішення власника (через координатора): SLP1 і великі літери з лабораторії UPC-14 прибрано; **для читання (документи, таблиці, тести, звіти) IAST першим, Деванагарі другим видом; джерела, що вже в Деванагарі (ashtadhyayi-data, Kāśikā), лишаються як є і цитуються без перекладу, IAST поруч** (остаточне уточнення власника 2026-10-01; воно скасовує проміжне «Деванагарі основне»); ідентичність = код. Виконувати має власник зони `prototype/` (координатор); тут лише план і перевірки.

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

## 2. Що робити з кожним файлом

| Файл | Дія |
|---|---|
| `ashtadhyayi-com-pratyahara.tsv` | **без SLP1**: перевибрати з першоджерела `ashtadhyayi-data/pratyahara/data.txt` (там уже Деванагарі: `name` «अण्», `list` «अ, इ, उ»; приголосні з вірамою «य्, व्, र्, ल्»). Колонки: `name_iast`, `start_iast`, `marker_iast`, `sounds_iast` (для читання, виводяться відображенням §3) і `name_deva`, `start_deva`, `marker_deva`, `sounds_deva` (як у джерелі). Початок = перший елемент `list`, маркер = остання літера `name` |
| `vidyut-sandhi-final-stops.tsv`, `vidyut-sandhi-vowels.tsv`, `paninian-verified-consonant-maps.tsv` | SLP1 → IAST і Деванагарі: колонки `first_iast`, `second_iast`, `result_iast`, `input_iast`, `output_iast` (для читання) і `…_deva` (другий вид) |

Для ashtadhyayi-com перетранслітерація через SLP1 не потрібна: менше кроків і менше помилок (SLP1-копія в репо сама була транслітерацією з Деванагарі).

## 3. Відображення SLP1 → IAST → Деванагарі (один символ SLP1 = один звук)

| SLP1 | IAST | Деванагарі | SLP1 | IAST | Деванагарі | SLP1 | IAST | Деванагарі |
|---|---|---|---|---|---|---|---|---|
| a | a | अ | k | k | क् | w | ṭ | ट् |
| A | ā | आ | K | kh | ख् | W | ṭh | ठ् |
| i | i | इ | g | g | ग् | q | ḍ | ड् |
| I | ī | ई | G | gh | घ् | Q | ḍh | ढ् |
| u | u | उ | N | ṅ | ङ् | R | ṇ | ण् |
| U | ū | ऊ | c | c | च् | t | t | त् |
| f | ṛ | ऋ | C | ch | छ् | T | th | थ् |
| F | ṝ | ॠ | j | j | ज् | d | d | द् |
| x | ḷ | ऌ | J | jh | झ् | D | dh | ध् |
| e | e | ए | Y | ñ | ञ् | n | n | न् |
| E | ai | ऐ | p | p | प् | b | b | ब् |
| o | o | ओ | P | ph | फ् | B | bh | भ् |
| O | au | औ | m | m | म् | y | y | य् |
| r | r | र् | l | l | ल् | v | v | व् |
| S | ś | श् | z | ṣ | ष् | s | s | स् |
| h | h | ह् | M | ṃ | ं | H | ḥ | ः |

`'` (avagraha) → `’` (IAST) і `ऽ` (Деванагарі). Приголосні в Деванагарі завжди з вірамою (звук, не склад), як у джерелі. `X` (довге ḷ) у даних не зустрічається (Kāśikā txt 389); якщо з'явиться, помилка, не мовчазна заміна.

## 4. Формат клітинки

Послідовність звуків пишеться за **форматом кодека** `encode_text`/`decode_text` (`prototype/upc14v2_script.py`, PR #62): токени **без пробілів**, середня крапка «·» лише там, де склейка читалася б інакше (IAST `k·h`/`kh`, `a·i`/`ai`; кирилиця `а·й`/`ай`); Деванагарі без роздільників (за правилами абугіди: `अइउ`, `क्ह्`); ліва й права частини результату sandhi через `|` (`d|a`, `द्|अ`). Усе в NFC. Перетворення робити саме через `transcode`/`encode_text`, а не власною таблицею (§3 лишається довідкою для SLP1).

## 5. Кроки

1. Скрипт `prototype/oracles/to_script.py` (зона координатора): (а) перевибір ashtadhyayi-com із першоджерела (Деванагарі) з виведенням IAST за §3; (б) SLP1→IAST і Деванагарі для трьох файлів за таблицею §3.
2. Одноразова перевірка перед видаленням оригіналів: зворотне відображення (IAST або Деванагарі → SLP1) має відтворити оригінал побайтово; для ashtadhyayi-com нові набори мають збігатися з рядками SLP1-файлу (за відображенням §3).
3. Заголовок кожного TSV: «Transliterated from SLP1 to IAST and Devanāgarī by `prototype/oracles/to_script.py`; original file at commit `<хеш>`, sha256 `<з §1>`» (для ashtadhyayi-com: «taken from ashtadhyayi-data/pratyahara/data.txt, commit 5744762f»); атрибуція upstream лишається.
4. SLP1-файли видаляються з дерева (історія git зберігає); оновити читачів (рядки в `test_upc14v2_oracles/sandhi/vowel_sandhi`); `test_upc14v2.py` перевести з `siva-sutras-encoded.yaml` на `ksetra/canon/siva-sutras.yaml` (IAST) або Деванагарі-джерело.
5. Прогнати тести: очікування те саме (13 + 26 + 22 + 29 OK на master; 97 з 99 і 127 з 154 + 27).

## 6. Ліцензія й провенанс

Дані `ashtadhyayi-com` без ліцензії: лише факти (назва й набір звуків). vidyut і paninian-verified (MIT): атрибуція в заголовку. Транслітерація не додає нового змісту.

## 7. Ризики

- Склеювання в IAST-виді: токени через пробіл; тести, що порівнюють склеєні рядки (`.text`, `mine == theirs`), перевести на списки токенів.
- Деванагарі: різниця між «звук» (`क्`) і «склад» (`क`); у даних тільки звуки (з вірамою), голосні без знаків залежних голосних.
- NFC: `ṛ`, `ṝ`, `ḷ` у IAST-виді; композитні знаки Деванагарі (ङ्, ऋ) у нормальній формі.
- `ऽ` (avagraha) у результатах vidyut: у Деванагарі `ऽ`, в IAST-виді `’`.

## 8. Готовий результат конвертації (2026-10-01)

Скрипт `docs/upc14-oracles-converted/to_script.py` (використовує `upc14v2_script.encode_text` на коміті `3785441`) вже перетворив усі 4 файли: `docs/upc14-oracles-converted/*.tsv` (IAST, Деванагарі, кирилиця; формат кодека). Кількість рядків збігається з SLP1-оригіналами (43, 99, 154, 32 + заголовки). Кожну клітинку розкодовано назад і порівняно з SLP1-оригіналом: розбіжностей 0 (інакше скрипт зупиняється). **Виправлення до §3:** у `vidyut-sandhi-vowels.tsv` і `…-final-stops.tsv` **є** довге ḷ (`X`, 11 і 1 рядок): кодек його не пише (Kāśikā txt 389: довгого ḷ нема), тому в TSV воно записане літералом ḹ / ॡ / л̣̄; авaграха `'` літералом ’ / ऽ. Це не звуки з 42; рішення, чи лишати такі рядки в оракулі, за власником `prototype/oracles/`. Файли треба скопіювати в `prototype/oracles/` координатором (його зона) і оновити читачів (назви колонок).
