# UPC-14: специфікація «кандидат» (агент «шіва», 2026-10-01)

Статус: **candidate**, не канон і не авторитет. Нічого не змінено в коді (`prototype/upc14v2*.py` лишається зоною координатора); зміни пропоную листом. Це опис наявного `prototype/upc14v2.py` на `origin/master` `d194378`, а не нового дизайну.

**Позначки:** `source-confirmed` = є в тексті Kāśikā (рядки `kAshikAvRRitti.txt`, «txt») або в сутрі; `empirically confirmed` = я або тест запускали й отримали результат (вказано що); `predicted` = випливає з моделі, але не перевірено окремим прогоном; `assumption` = моделювальний вибір без джерела в корпусі.

## 1. Розкладка 14 біт

`code = meta(1) | place(5) | nasal(1) | aperture(3) | length(2) | voice(1) | asp(1)` (зсуви 13 / 8 / 7 / 4 / 2 / 1 / 0; `upc14v2.py`).

| Біти | Поле | Значення |
|---|---|---|
| 13 | meta | 1 = клітина-маркер на шляху сутр (не звук) |
| 12-8 | place | булева ґратка на 5 атомах K T M D O (горло, піднебіння, мозок, зуби, губи); join = OR; `v` = D + O |
| 7 | nasal | окремий атом від місця (1.1.8) |
| 6-4 | aperture | шлях 0 stop, 1 semivowel, 2 sibilant, 3 vowel, 4 wide vowel |
| 3-2 | length | шлях 0 short, 1 long, 2 pluta |
| 1 | voice | ребро unvoiced–voiced |
| 0 | asp | ребро unaspirated–aspirated |

Ідентичність клітини = **координати вершини**, не номер у таблиці і не рядок.

## 2. Інваріанти

| # | Інваріант | Позначка |
|---|---|---|
| I1 | Недійсний код (немає articulator, поза шляхом, приголосний із length, meta як звук) **не ремонтується**: `InvalidCode` | empirically confirmed (`test_upc14v2.py`, 29 OK на master) |
| I2 | 42 звуки мають 42 різні коди; жодна мітка не є ідентичністю (мітки лише IAST/Деванагарі; SLP1 і великі літери прибрано рішенням власника 2026-10-01) | empirically confirmed (там само) |
| I3 | Весь інвентар виводиться з насіння `k` типізованими ребрами (asp, voice, nasal, shift, lift, join, long); жоден звук не заданий списком ознак | empirically confirmed (`DERIVATION`, тести); вхід, який лишається: насіння, типи ребер, порядок сутр |
| I4 | Pratyāhāra = інтервал шляху сутр; маркер = meta-клітина; сам маркер не входить | source-confirmed (1.1.71, txt 1647); empirically confirmed: 43 із 43 `ashtadhyayi.com`; 42 із 42 записів `pratyahara-usage.yaml` **після виправлення** (мій прогін 2026-10-01 на гілці `fix/48-53-…`; у master YAML ще має 3 хибні записи → 39 з 42) |
| I5 | Savarṇa = рівні place і aperture: **одна бітова маска `0x1F70`** (place 5 біт + aperture 3 біти, розділені бітом nasal) | source-confirmed як зміст 1.1.9 (txt 375-384 «tulya āsye prayatnaḥ»); empirically confirmed як маска: `savarna()` == `(a&0x1F70)==(b&0x1F70)` на всіх 47×47 парах (мій прогін, `docs/upc14-prana14-vs-v2-2026-10-01.md`) |
| I6 | Savarṇa не охоплює ṛ~ḷ без вартіки (`vartika=True` додає) | source-confirmed (txt 400-403, 53198, 53396); 1.1.9 як написано їх не називає |
| I7 | e≁ai, o≁au (aperture 3 проти 4) | assumption. Kāśikā каже лише, що e o ai au мають по 12 видів і не мають коротких (txt 390); «e не savarṇa до ai» там нема. Siddhāntakaumudī і Laghukaumudī (`ashtadhyayi-data`, ключ 11009) дають e і ai одне місце (kaṇṭhatālu), o і au kaṇṭhoṣṭha; обидва в чотирьох чи п'яти ābhyantara-prayatna лишають e і ai vivṛta; за самим означенням 1.1.9 вони були б savarṇa. Mahābhāṣya (ключ 11009, у запереченні) називає ai/au «vivṛtatara» щодо a, про e~ai нічого. Пряме джерело не знайдено |
| I8 | 1.1.50: заміна = найближча вершина цільової множини; нічия → `Ambiguous`, не вибір | empirically confirmed на yaṇ/jaś/car/cu/wu; поза доменом правила нічия очікувана (мій прогін) |
| I9 | Довжина = координата; довгого ḷ нема (`dirgha(ḷ, ḷ)` кидає) | source-confirmed (txt 389 «लृवर्णस्य दीर्घा न सन्ति») |
| I10 | Результат правила з опцією «vā» = множина варіантів, жоден не головний | predicted (так сформульовано в специфікації; код віддає `sounds` + `options`) |

## 3. Що виводиться з графа, а що припущення

| Твердження | Статус | Джерело / примітка |
|---|---|---|
| 42 звуки з насіння `k` | empirically confirmed | I3 |
| Pratyāhāra як інтервал | source-confirmed + empirically confirmed | I4 |
| Savarṇa як маска | source-confirmed + empirically confirmed | I5 |
| guṇa/vṛddhi як join місць | **trivial by construction** (визначені так) | не доказ |
| yaṇ/jaś як `nearest` | empirically confirmed | 1.1.50 |
| Місце кожного звука (K T M D O) | assumption | традиційна класифікація; sthāna не перевірено в корпусі для всіх звуків |
| Голос/придих ś ṣ s h (aghoṣa mahāprāṇa; h ghoṣa mahāprāṇa) | assumption | Śikṣā/Siddhāntakaumudī; у Kāśikā не знайдено (пошук за महाप्राण/अल्पप्राण/घोष/अघोष) |
| h = горло, підйом gh | assumption | традиція; у корпусі не звірено |
| **Aperture-розщеплення: sibilant = 2, vowel = 3** | **source-confirmed поза Kāśikā; assumption щодо Kāśikā** | Kāśikā (txt 386) і Siddhāntakaumudī називають чотири ābhyantara-prayatna (spṛṣṭa, īṣatspṛṣṭa, saṃvṛta, vivṛta): ūṣman і голосні обидва vivṛta. **Laghukaumudī** (`laghukaumudi.txt`, ключ 11009) дає п'ять: spṛṣṭa, īṣatspṛṣṭa, **īṣadvivṛta (ūṣman)**, **vivṛta (голосні)**, saṃvṛta; це джерело розщеплення 2/3. Для Kāśikā лишається альтернативне читання: розділяє їх 1.1.10 «na ajjhalau» (txt 410) |
| a = aperture VOWEL (3) | source-confirmed | txt 29-33: коротке a saṃvṛta в вжитку, але в шастрі розглядається як vivṛta для savarṇa; 8.4.68 повертає |
| ai/au = п'ятий ступінь aperture (4) | assumption | Śikṣā-традиція; не з Kāśikā |
| `v` = D + O (зуби + губи) | assumption | традиція (dantoṣṭhya) |
| Порядок ознак після place у `nearest` (aperture, voice, asp, nasal, length) | assumption | у Kāśikā не знайдено; варто фіксувати як припущення |
| Порядок сутр | вхід (канон) | `ksetra/canon/siva-sutras.yaml` |
| Маркери = останній hal сутри (14 шт.) | source-confirmed | 1.3.3 (txt 3349-3366), перші чотири названі явно; решта 10 за тим самим правилом |
| aṇ = перший ṇ, iṇ = другий; виняток aṇ у 1.1.69 | source-confirmed | txt 99-103, 1622-1623, 43710 |
| Друге h | source-confirmed | txt 165-176 |

## 4. Оракули

| Оракул | Результат | Позначка |
|---|---|---|
| `ashtadhyayi.com` pratyāhāra (`oracles/ashtadhyayi-com-pratyahara.tsv`) | 43 із 43 інтервали | empirically confirmed |
| `pratyahara-usage.yaml` (ksetra) | 39 із 42 на master; 42 із 42 після виправлення | empirically confirmed |
| vidyut, кінцеві k ṭ t p (`vidyut-sandhi-final-stops.tsv`) | 97 із 99; 2 розбіжності = вибір порядку правил | empirically confirmed (тести координатора) |
| vidyut, голосні (`vidyut-sandhi-vowels.tsv`) | 127 із 154; 27 розбіжностей усі e/ai, = опційне випадіння y (8.3.19); vidyut елідує лише y, Kāśikā дозволяє y і v (txt 80714) | empirically confirmed (мій незалежний прогін) |
| paninian-verified (Coq) | прочитано, Coq не запускали; v2 відходить у `voiced_of` (kh→gh) і блокувальниках ṇatva (kṛśānu) | read, not run |
| Приклади Kāśikā (сандхі) | таблиці в `docs/upc14v2-kasika-*-sandhi-…md` | source-confirmed |
| `savarna_str` vidyut | містить ṛ~ḷ | read |
| SandhiKosh (.xls) | не розібрано | not checked |
| PRĀṆA-14 (`prana14.py`) savarṇa | ті самі 22 класи, 0 розбіжностей (42×42), крім вартіки ṛ/ḷ | empirically confirmed |

## 5. Що специфікація НЕ стверджує

Історичний задум Паніні; апаратну упаковку чи швидкодію (нічого не виміряно; «слово 32 = 4 тег + 28 значення = 2×14» це арифметика); повну граматику (порядок правил 1.4.2, наголос, опційність vā поза моделлю); фонетичну точність ознак (модель перевірена на внутрішню несуперечність).

## 6. Нотація (рішення власника 2026-10-01: без SLP1 і великих літер; **IAST першим** (малі літери з діакритикою; власнику так легше читати), **Деванагарі другим видом**; ідентичність = код; джерела, що вже в Деванагарі, цитуються як є, IAST поруч)

Усі значення нижче: **мітки для людей і тестів**, не ідентичність. Позначки: `source-confirmed` = уживається в корпусі Kāśikā (`kAshikAvRRitti.txt`, лічено мною 2026-10-01); `hypothesis` = пропозиція без джерела в корпусі.

| Явище | IAST | Деванагарі | Позначка і джерело |
|---|---|---|---|
| Довгі голосні | ā ī ū ṝ | आ ई ऊ ॠ | source-confirmed (текст Kāśikā); довгого ḷ нема (txt 389) |
| Анусвара | ṃ | ं (U+0902) | source-confirmed: 13159 уживань у txt; Laghukaumudī 1.1.9 «अं अः» |
| Вісарга | ḥ | ः (U+0903) | source-confirmed: 31759 уживань у txt |
| Аваграха | ’ | ऽ (U+093D) | source-confirmed: 2916 уживань у txt |
| Pluta | голосний + цифра 3 (a3, bho3i) | голосний + ३ (U+0969), напр. भो३इ | source-confirmed: 6451 уживань ३ у txt; `KASIKA-6.1.77.yaml` «bho3i, bho3yindram» |
| Назалізація (анунасіка/чандрабінду) | голосний + U+0303 (ã) або m̐ | ँ (U+0901) після голосного | **hypothesis**: у Kāśikā txt 0 уживань ँ і 0 U+0303; запис за звичаєм Unicode/ISO 15919 (не читано тут), рішення власника. Kāśikā лише каже, що y v l мають носові форми (txt 391) і що ḷ анунасіка за pratijñā (txt 107) |
| Jihvāmūlīya, upadhmānīya | не пропоную | ᳵ ᳶ | не уживаються в txt (0); Laghukaumudī пише їх «≍क», «≍प»; поза обсягом 42 звуків |

Правила запису: (1) усі літери малі; (2) тексти нормалізуються в NFC; (3) **послідовності звуків пишуться токенами через пробіл** (IAST неоднозначний при склеюванні: `kh` проти `k h`, `ai` проти `a i`); (4) лише Деванагарі і IAST у документах, SLP1 лишається тільки в історії git.
