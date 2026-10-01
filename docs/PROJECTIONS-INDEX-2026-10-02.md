# Кластер проекцій: що є, де, статус (індекс, 2026-10-02)

Статус: **індекс, не authority**. Одна сторінка про UPC-14 (граф звуків), 7-бітні проєкції і мовні шари. Усі шляхи від кореня `shiva-sutras`. Статуси: **canon** (закріплено власником/SENS), **candidate** (кодується, перевірено, рішення за власником), **research** (гіпотеза, довідка), **record** (журнал, історія).

## 1. 14-бітний граф звуків (UPC-14 v2)

| Що | Де | Статус |
|---|---|---|
| Специфікація і код графа (42 звуки, ребра, pratyāhāra, savarṇa) | `prototype/UPC14-v2.md`, `prototype/upc14v2.py` | candidate |
| Закон: кожне ребро це одна бітова операція | `prototype/upc14v2_bitops.py`, `docs/upc14-bit-edge-laws-2026-10-02.md` | research |
| Кодек тексту: IAST, деванагарі, кирилиця, pluta | `prototype/upc14v2_script.py`, `docs/upc14-script-codec-fuzz-2026-10-01.md` | candidate |
| Приголосне і голосне сандхі | `prototype/upc14v2_sandhi.py`, `prototype/upc14v2_vowel_sandhi.py`, `docs/upc14v2-kasika-consonant-sandhi-2026-09-30.md`, `docs/upc14v2-kasika-vowel-sandhi-2026-09-30.md` | candidate |
| Оракули (IAST/деванагарі), їхній план і конвертація | `prototype/oracles/`, `docs/upc14-oracles-iast-plan-2026-10-01.md`, `docs/upc14-oracles-converted/` | candidate |
| Стан, джерела, відкриті рішення | `docs/upc14-status-and-sources-2026-10-01.md` (згорнуто в `UPC14-v2.md`), `docs/upc14-open-decisions-2026-10-01.md`, `docs/upc14-candidate-spec-2026-10-01.md` | record / candidate |
| Незалежна рев'ю, граф апавад | `docs/upc14v2-independent-review-2026-09-30.md`, `docs/upc14v2-apavada-graph-check-2026-09-30.md` | record |
| Порівняння кодеків (prāṇa14, varṇa7 та ін.) | `docs/upc14v2-codecs-comparison-2026-10-01.md`, `docs/upc14-prana14-vs-v2-2026-10-01.md` | research |
| Кирилиця: джерело і перевірка | `docs/upc14-cyrillic-source-bhagavad-gita-2026-10-01.md`, `docs/upc14-cyrillic-check-2026-10-01.md` | candidate (ṅ ñ ṇ: hypothesis) |

## 2. 7-бітні проєкції

| Що | Де | Статус |
|---|---|---|
| Закріплена таблиця UPC-7 (SENS пінить за sha) | `prototype/upc7-table.tsv`, `prototype/upc7-table.sha256`, `prototype/UPC7.md`, `prototype/UPC7-GEOMETRY-v2.md` | **canon** (SENS Text7) |
| saṅkṣepa7: клітинки з графа (43 з 46 збігаються з ручною; r, l, h різні) | `prototype/upc7_derive.py`, `docs/upc7-sankshepa7-impact-on-sens-2026-10-01.md` | candidate; міграція SENS: рішення власника (рекомендація: не мігрувати) |
| Огляд усіх 7-бітних прототипів і вартість запитів | `prototype/survey_7bit.py`, `prototype/bench_7bit/`, `docs/upc7-prototypes-survey-2026-10-01.md`, `docs/upc7-design-query-bench-2026-10-01.tsv` | research |
| Мовно-відповідна таблиця (українська / санскритська розкладка) | `prototype/upc7_lang.py`, `prototype/uk_orth.py`, `prototype/upc7-table-v3.tsv`, `docs/upc7-language-table-2026-10-02.md` | candidate; закріплену таблицю не змінює |
| Санскрит проти української: звуки, IPA, джерела | `docs/sanskrit-ukrainian-sounds-2026-10-02.md` (+ `.tsv`) | research (IPA: зовнішня конвенція) |

## 3. Рішення і узгодження

| Що | Де |
|---|---|
| Порядок мержу і стан PR | `docs/MERGE-SCREEN-2026-10-01.md` (історична після мержу) |
| Питання власнику з рекомендаціями | `docs/OWNER-QUESTIONS-2026-10-02.md` |
| Звірка тверджень у SENS, рев'ю `bench_7bit` | `docs/sens-claims-check-and-pr65-review-2026-10-01.md` |
| Журнали роботи | `docs/upc14v2-work-log-2026-09-30.md`, `docs/upc14-work-record-2026-09-30.md` |

## 4. Тести

`cd prototype && python3 -m unittest discover -s . -p 'test_*.py'` (250+ тестів). CI: `.github/workflows/upc7-prototype.yml` (UPC-7, UPC-14 v2, derive, language layer). Окремо `tests/` (потрібен `yaml`); 2 давні падіння `test_epistemic_linter` чекають рішення власника.
