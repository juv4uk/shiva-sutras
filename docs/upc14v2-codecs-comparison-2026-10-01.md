# Порівняння кодеків на master з UPC-14 v2 (агент «шіва», 2026-10-01)

Статус: **огляд без оцінок «краще/гірше»**, лише читання. Джерело: `origin/master` `9552865` (merge «codec refresh with graph-based codecs»). Файли: `prototype/upc14v2.py` (еталон порівняння), `graph14.py` (bandha14), `graph7.py` (tantu7), `trishula14.py` (triśūla14), `akshara7.py` (akṣara7), `varna7-prana14/{prana14.py,varna7.py,varna7_table.py,varna7-table.tsv,README.md}` (prāṇa14, varṇa7), `GRAPH7_BANDHA14.md`, `AKSHARA7_TRISHULA14.md`. Тести кодеків я не запускав.

Мітки: **(г)** звуки виведені з графа; **(т)** звуки задані таблицею або літеральним списком; **(гр)** кодек за задумом каже «граф».

## 1. Розкладка 14 біт

| Кодек | Біти (від старшого) | Що кодує клітина |
|---|---|---|
| **upc14v2** | meta(1) \| place(5) \| nasal(1) \| aperture(3) \| length(2) \| voice(1) \| asp(1) | звук (координати ознак) або meta-клітина маркера |
| **prāṇa14** | meta(1) \| effort(2) \| wide(1) \| place(5) \| nasal(1) \| prāṇa(2) \| length(2) | звук (координати ознак); voice+asp упаковано в одне поле prāṇa; місця в тих самих 5 атомах |
| **triśūla14** | kind(3) \| index(5) \| variant(3) \| voice(1) \| aspiration(1) \| length(1) | запис ознак: тип, локальний індекс, варіант |
| **bandha14** | source(6) \| target(6) \| relation(2) | **ребро** `source → target` із типом (sutra, varga, lift, reverse) |

7-бітні: tantu7 = vertex(6) + meta(1) (номер звука); akṣara7 = family(2) + payload(5); varṇa7 = region(2) + payload(5), регіони за prayatna.

## 2. Як з'являються 42 звуки

| Кодек | Звуки | Ознака |
|---|---|---|
| upc14v2 | з одного насіння `k` типізованими ребрами (asp, voice, nasal, shift, lift, join, long) | **(г)** |
| prāṇa14 | з насіння `k` типізованими ребрами (asp, voice, nasal, shift, lift, widen, join, long); 47 звуків (42 + 5 довгих) | **(г)** |
| triśūla14 | літеральний словник `FEATURES` («complete canonical inventory»); `_stop(place, member)` лише скорочує запис | **(т)** |
| bandha14 | літеральний кортеж `SOUNDS`: індекс = номер вершини | **(т)** для вершин; **(г)** для ребер (див. §5) |
| tantu7 | той самий кортеж `SOUNDS` (індекс 0..41) | **(т)** |
| akṣara7 | кортеж `SOUND_ORDER` + шлях сутр; клітина = позиція | **(т)** |
| varṇa7 | таблиця `varna7-table.tsv` із sha256 (`varna7_table.py`) | **(т)** |

Порядок вершин у `SOUNDS` graph7/graph14/akshara7 **не збігається з порядком Шіва-сутр** (там `… n, j, jh, b, bh, g, gh, k, kh, c, ch, ṭ, …`, а не `jh bh / gh ḍh dh / j b g ḍ d / kh ph …`), тож код вершини не є рангом на шляху.

## 3. Pratyāhāra як інтервал шляху сутр

| Кодек | Чи є | Як |
|---|---|---|
| upc14v2 | так | інтервал на шляху; маркер = meta-клітина; `nth` для повторних маркерів; `strict` для h |
| prāṇa14 | так | `pratyahara(start, marker, nth, start_occurrence, strict)`: інтервал `PATH`, маркери не входять; сигнатура та поведінка такі самі, як у upc14v2 |
| triśūla14 | так | `pratyahara(start, marker)` по окремому кортежу `SUTRAS`; шлях не закодований у клітині; `nth` нема |
| akṣara7 | так | `pratyahara(start, marker, occurrence)` по `_path()`; маркер = meta-клітина (family 01) |
| bandha14, tantu7 | **ні** (`pratyahara` не зустрічається) | ребро `sutra` = сусідство в рядку сутри; інтервалу нема |
| varṇa7 | не в `varna7.py`; `compare_to_upstream.py` порівнює з інтервалами prāṇa14 | |

## 4. Savarṇa і запити

| Кодек | savarṇa | Запити 1.1.50, guṇa/vṛddhi |
|---|---|---|
| upc14v2 | функція: те саме місце й aperture; ṛ~ḷ лише з `vartika=True` | `nearest` (Ambiguous на нічиїй), guṇa/vṛddhi як join місць |
| prāṇa14 | маска `(a & 0x1FE0) == (b & 0x1FE0)` = effort+wide+place (біти 5-12); `e~ai` **False** завдяки біту wide | `nearest`, guṇa, vṛddhi, dirgha |
| varṇa7 | `savarna_key`; `e~ai` **True** («межа 7 біт», як і в UPC-7, записано в README) | немає |
| triśūla14, bandha14, tantu7, akṣara7 | не реалізовано | не реалізовано |

## 5. Граф чи таблиця (за словами власника «UPC-14 буде каноном, граф, не таблиця»)

| Кодек | Опора на «граф» | Що лишається таблицею |
|---|---|---|
| upc14v2 | звуки виведені з насіння (г); pratyāhāra = інтервал шляху; запити = найближча вершина | ознаки сутностей (місце, aperture, voice, asp) як моделювальний вибір |
| **prāṇa14** | те саме за структурою (г); ребра derivation у `DERIVATION`, `--dot` виводить граф | ознаки як моделювальний вибір |
| **bandha14** | клітина є ребром (гр); ребра sutra і varga виводяться з шляху й рядків | вершини = літеральний кортеж; ребра `lift` виписані вручну; pratyāhāra нема |
| **tantu7** | клітина = вершина; ребра виводяться (`graph_edges`) | вершини = літеральний кортеж; `lift` виписані вручну |
| triśūla14 | шлях використано лише для pratyāhāra | інвентар = таблиця (т); ознаки літеральні |
| akṣara7 | шлях сутр і meta-клітини маркерів | інвентар = таблиця (т) |
| varṇa7 | — | інвентар = таблиця (т) |

## 6. Розбіжності в ознаках, які видно з коду (без оцінки)

- **lift-зв'язки.** graph7/graph14 виписують вручну пари `(a, ai) (a, au) (i, y) (u, v) (ṛ, r) (ḷ, l) (e, ai) (o, au) (j, y) (d, r) (b, v)`; upc14v2 виводить `y` від `j`, `r` від `ḍ`, `l` від `d`, `v` від `b` + зуби, голосні від voiced-stop з aperture+3. У graph7 пара `(d, r)` (d → r), у upc14v2 `r` від `ḍ`.
- **aperture/effort.** upc14v2: 0 stop, 1 semivowel, 2 sibilant, 3 vowel, 4 wide vowel (3 біти); prāṇa14: effort 0-3 (spṛṣṭa, īṣat-spṛṣṭa, ūṣman, vivṛta) + окремий біт wide (e/o від ai/au). Kāśikā (рядок 386 txt) називає чотири ābhyantara-prayatna; розділення ūṣman і голосних у upc14v2 записано як припущення.
- **voice/asp.** upc14v2: два окремі біти; prāṇa14: поле prāṇa(2): aghoṣa/ghoṣa × alpa/mahā; triśūla14: окремі voice і aspiration.
- **Довгі голосні.** prāṇa14 матеріалізує 47 (довгі a i u ṛ ai au); upc14v2 тримає 42 + length-координату; ḷ без довгого в обох (Kāśikā txt 389).

## 7. Спостереження про походження (факт, без висновків)

`prana14.py` збігається з `upc14v2.py` структурою й частиною тексту: із 250 не тривіальних рядків (довших за 25 знаків) upc14v2.py **92 зустрічаються дослівно** в prana14.py (включно з boilerplate: імпорти, рядки `raise InvalidCode(...)`, `unpack`, зсуви полів); однакові `VARGA_FIRST`, `VARGA_ROWS` (SLP1), `_derive` від насіння `k`, сигнатура `pratyahara(start, marker, nth, start_occurrence, strict)`. README називає кодеки «my design» і «самостійні альтернативи»; у коментарях файлу prana14.py я не знайшов згадки, що структуру взято з upc14v2. Автор коміту `6a1f5b4`: juv4uk (той самий git-користувач, що й у цій сесії). Чи це питання ліцензії/авторства, я не оцінюю.

## 8. Що не перевірив

Тести кодеків (`test_graph_codecs.py`, `test_akshara7_trishula14.py`, `test_my_codecs.py`) і `compare_to_upstream.py` не запускав; порівняння `upc14v2` ↔ `prana14` на всіх парах не повторював; tantu7 і bandha14 читав до `pratyahara` (його там нема), а не до кінця файлу; `varna7.py` читав лише шапку.
