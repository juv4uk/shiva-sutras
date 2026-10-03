# Text7 geometry: candidate D ratification record (2026-10-03)

Українська версія — нижче (розділ «Українською»).

Scope: choice of the 7-bit geometry for Text7 (UPC-7). Reproduce everything with
`python3 prototype/criterion_b_generator_diff.py`, `criterion_a_savarna_eval.py`,
`criterion_c_anti_numerology.py`, `test_sandhi_roundtrip_guna.py` (all stdlib, seconds).
Refs #2497 #2494 #2490.

## 1. Result in one table

| Criterion | H (hand) | D (derived) | V (varṇa7) |
|---|---|---|---|
| (b) cells equal to D | 43/46 | — | 41/42 shared sounds |
| (a) strict 1.1.9 matrix, 1764 pairs | 1758 (6 errors) | 1760 (4 errors) | 1760 (4 errors) |
| (a) Vidyut vowel corpus | 19/23 recall, FP 3, FN 4 | 19/21 recall, FP 3, FN 2 | 19/23 recall, FP 3, FN 4 |
| (c) positive-class F1 vs 10 000 permutations | — | 0.987 vs best 0.449 | — |

Correction of the first PR text: the corpus result is **not** 100%. It is 138/143 correct
for D (ḹ rows skipped, see 2). Accuracy alone is also not a discriminating metric
against permutations (mean 90.15% from true negatives); the F1 above is.
Candidates are not compared on identical row sets for ḹ: D has no ḹ cell (Kāśikā: no such sound),
H and V do, so their FN count includes ṛ~ḹ / ṝ~ḹ.

## 2. Provenance pins (condition 1)

| File | sha256 | Upstream |
|---|---|---|
| `prototype/oracles/vidyut-sandhi-vowels.tsv` | `7d44aae736efd01dcaa0b37431451ebfa9fa66adf636b417a2bebd140cc49f71` | ambuda-org/vidyut, `vidyut-sandhi/src/generator.rs`, commit `8da2f90bee3ce1c07505fa432fc3729e3f7e02ea` |
| `prototype/oracles/paninian-verified-consonant-maps.tsv` | `aae2fdeaee5c2a2adefb26910b94e2dd05860178785c2b1b33c3e12ee103855e` | CharlesCNorton/paninian-verified, commit `9d2e3efa7c77ac2f3310f657406afdddd6bd4b61` |

Corpus size: 154 rows, 11 skipped (all involve ḹ), 143 evaluated. Any change of these hashes
invalidates the numbers in section 1 until the scripts are rerun.

## 3. Documented limit: e~ai, o~au (condition 2)

Four ordered pairs remain wrong under strict 1.1.9 for D and V: (e, ai), (ai, e), (o, au), (au, o).
This is not a defect to repair. guṇa and vṛddhi share one vowel row and differ only by the length
bit; 1.1.9 savarṇa ignores length, so a one-cycle bit test cannot separate them. Adding bits to
"fix" it would spend reserved cells and violate #2494. Two further corpus "misses", ṛ~ḷ, exist only if the vārttika is used as ground truth (as
`criterion_a_savarna_eval.py` does): vidyut itself does NOT merge ṛ+ḷ (`r|ḷ`), and Text7 rows differ, so Text7
agrees with 1.1.9 and with vidyut. Against vidyut's own behaviour D has no false negative on the
`ak`+`ak` rows. Classified in `prototype/test_savarna_dirgha_layers.py` (layer 1 asserted: 70 rows, 16 merges;
layer 2 vārttika and layer 3 diphthongs annotated). Corpus coverage limit: no row has `o` or `ḷ` as the first
vowel, so (o,au) is covered only by the pair matrix.
What Text7 does not express structurally, D14 expresses through context (the 43-node Śiva-sūtra
graph with h₁/h₂, see `hakardvitva-c1p-topological-necessity.md` and sens
`docs/research/2497-d7-d14-constitutional-demarcation.md`). Do not change Text7 bits for this.

## 4. Status of the six 7-bit prototypes (condition 3)

| Proto | Status | Reason (measured) |
|---|---|---|
| H | archive | 3 documented errors vs D: r (dental, contradicts 1.1.9 ṛṭuraṣāṇāṁ mūrdhā), l (invented lateral slot, scar of the r error), h (invented glottal place) |
| **D** | **chosen** | derived from the UPC-14 graph, fewest errors; 43/46 equal to H |
| V | rejected as an independent choice; kept as cross-check | equals D on 41 of 42 sounds; differs only on `l` (V keeps H's lateral slot 0101111, D 0101110); also carries ḹ, which the Kāśikā denies |
| A, T | closed | A and T are identical on 42/42; sūtra-order codes, 25/43 pratyāhāras contiguous, no articulatory geometry |
| L | not a Text7 candidate | sūtra order, 39/43 contiguous = the ceiling proved in PR #113; belongs to D14, not Text7 |

Caveat on evidence: the savarṇa predicate in criterion (a)/(c) reads bit fields of the same
structure D was derived from, so D passing is partly by construction. The independent evidence
is (b) (agreement with 1.1.9 text and with V, which was designed separately) and the sandhi
corpus, not the permutation test alone.

## Українською

Область: вибір 7-бітної геометрії Text7 (UPC-7). Усе відтворюється чотирма скриптами
(див. вище), лише stdlib. Refs #2497 #2494 #2490.

**Виправлення першого тексту PR.** Результат на корпусі Vidyut — **не** 100%: для D це 138/143
правильних (рядки з ḹ пропущено). Точність сама по собі не відрізняє від перестановок
(середнє 90,15% дають істинні негативи); відрізняє F1 по позитивному класу: D = 0,987
проти найкращої з 10 000 перестановок = 0,449. Покриття ḹ неоднакове: у D немає клітинки ḹ
(Кашіка: такого звуку немає), у H і V вона є, тож їхні FN включають ṛ~ḹ / ṝ~ḹ.

**Пін походження (умова 1).** `vidyut-sandhi-vowels.tsv` sha256
`7d44aae7…cc49f71` (ambuda-org/vidyut, коміт `8da2f90b…`);
`paninian-verified-consonant-maps.tsv` sha256 `aae2fdea…e103855e`
(CharlesCNorton/paninian-verified, коміт `9d2e3efa…`). Корпус: 154 рядки, 11 пропущено
(усі з ḹ), 143 оцінено. Зміна хешу робить числа недійсними до повторного прогону.

**Задокументована межа (умова 2).** Чотири впорядковані пари (e,ai), (ai,e), (o,au), (au,o)
лишаються «помилкою» за суворою 1.1.9 для D і V. Це не дефект: гуна і вріддгі ділять один
рядок голосних і різняться лише бітом довжини, а савarṇa 1.1.9 довжину ігнорує, тож
однотактний бітовий тест їх не розрізнить. Додавання бітів «для виправлення» витратило б
зарезервовані клітинки й порушило б #2494. Ще два «промахи» корпусу, ṛ~ḷ, існують лише
якщо за еталон взято вартику (так робить `criterion_a_savarna_eval.py`): сам vidyut ṛ+ḷ НЕ зливає
(`r|ḷ`), а рядки Text7 різні, тож Text7 узгоджений і з 1.1.9, і з vidyut. Відносно власної
поведінки vidyut D не має хибнонегативних на парах ak+ak. Класифікація —
`prototype/test_savarna_dirgha_layers.py` (шар 1 стверджується: 70 рядків, 16 зливань; шар 2 вартика
і шар 3 дифтонги анотуються). Межа покриття корпусу: жоден рядок не має `o` чи `ḷ` першим голосним,
тож (o,au) покрито лише матрицею пар. Те, чого Text7 не виражає структурно,
виражає D14 через контекст (43-вузловий граф Шива-сутр з h₁/h₂). Біти Text7 через це не змінювати.

**Статус шести прототипів (умова 3).** H — архів (три задокументовані помилки: r, l, h).
**D — обраний.** V — не обирається як самостійний, лишається перехресною перевіркою:
збігається з D на 41 з 42 звуків, відрізняється лише на `l` (V тримає штучний слот
«lateral» 0101111 від H) і містить ḹ, якого Кашіка не визнає. A і T ідентичні (42/42),
це порядок сутр без артикуляційної геометрії. L — порядок сутр, 39/43 суміжних =
доведена у PR #113 межа; належить D14, а не Text7.

**Застереження щодо доказів.** Предикат savarṇa у критеріях (а)/(в) читає бітові поля тієї
самої структури, з якої виведено D, тож проходження D частково побудоване. Незалежні докази —
критерій (б) (збіг із текстом 1.1.9 та з V, спроєктованим окремо) і сандхі-корпус, а не
лише перестановковий тест.
