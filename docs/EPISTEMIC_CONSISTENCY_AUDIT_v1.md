# Epistemic Consistency Audit v1

**Дата:** 2026-08-16  
**Аудитор:** sarvam-ai (зовнішній агент)  
**Repository:** juv4uk/shiva-sutras @ 636af77  
**Scope:** Усі authoritative/operational артефакти репозиторію  
**Тип:** Діагностичний документ — лише фіксація, без виправлень

---

## Методологія

Аудит перевіряє дві речі:

1. **Чи суперечать файли один одному?** — формальні конфлікти статусів, тверджень, директив.
2. **Чи може новий агент, читаючи репозиторій у рекомендованому порядку, однозначно визначити актуальний стан?** — навігаційна ясність.

Кожна знахідка класифікована за типом і має однаковий формат.

---

## Знайдені проблеми

### ECA-001

```yaml
id: ECA-001
severity: high
type: STATE_CONTRADICTION
subject: stage-6-freeze-status

files:
  - path: FREEZE_STAGE_6_0.md
    statement: "Stage 6.0 frozen. next_allowed_trigger: externally attributable corpus."
    frozen_commit: "TBD"  # ніколи не заповнено

  - path: RESEARCH_MAP.md
    statement: "Доступний незалежний корпус (Provenance) — RESOLVED. GRETIL Kāśikāvṛtti + Aṣṭādhyāyī Baums; manifest + sha256."

  - path: .agents/rules/epistemic_agent.md
    statement: "Stage 6.0 заморожено. Подальший прогрес щодо лінгвістичної незалежності канонічної моделі заблоковано до появи зовнішнього, незалежно атрибутованого історичного корпусу."

  - path: docs/research-index.md
    statement: "Розділ 7: Статус 🟢 ВИРІШЕНО (AUTHENTICITY-VERIFIED (Attributed))"

  - path: journal/0008-gretil-corpus-gate.yaml
    statement: "status: EVIDENCE-LOGGED. GRETIL Kāśikāvṛtti (Sharma ed.) + Aṣṭādhyāyī (Baums) acquired with sha256 manifest."

  - path: journal/07_epistemic_rearming.md
    statement: "We did NOT unfreeze Stage 6.0. State: FROZEN -> ARMED / WAITING_FOR_CORPUS."

why_inconsistent: >
  Тригер FREEZE_STAGE_6_0.md (наявність зовнішнього атрибутованого корпусу)
  виконано — journal 0008 фіксує acquisition GRETIL свідків з sha256 manifest.
  RESEARCH_MAP позначає це як RESOLVED. Проте:
  (a) FREEZE_STAGE_6_0.md не має supersedes/superseded_by поля і не позначений
      як історичний;
  (b) epistemic_agent.md досі наказує агенту вважати Stage 6.0 замороженим;
  (c) journal 07 (написаний ДО journal 0008) каже "did NOT unfreeze", але
      journal 0008 (пізніший) вже фіксує виконання тригера — без UNFREEZE документа;
  (d) frozen_commit: "TBD" ніколи не заповнено.

epistemic_risk: >
  Новий агент, читаючи epistemic_agent.md, буде діяти так, ніби Stage 6.0
  заморожено, хоча фактично тригер виконано. Це може призвести до відмови
  від легітимної роботи з real corpus або, навпаки, до ігнорування обмежень,
  які ще актуальні (наприклад, L-001 досі OPEN).

recommended_resolution: >
  1. Створити STAGE_6_1_ACTIVATION.md: який trigger, яким evidence,
     на якому commit, що розблоковано, що залишилось забороненим.
  2. Позначити FREEZE_STAGE_6_0.md як status: superseded, superseded_by: STAGE_6_1_ACTIVATION.md
  3. Оновити .agents/rules/epistemic_agent.md: замінити "Stage 6.0 заморожено"
     на актуальний стан.
  4. Заповнити frozen_commit у FREEZE_STAGE_6_0.md.

must_not_do:
  - Видалити FREEZE_STAGE_6_0.md
  - Переписати journal 07 так, ніби він ніколи не казив "not unfreeze"
  - Переписати RESEARCH_MAP ретроактивно
```

---

### ECA-002

```yaml
id: ECA-002
severity: high
type: STALE_DIRECTIVE
subject: agent-rule-frozen-but-corpus-resolved

files:
  - path: .agents/rules/epistemic_agent.md
    statement: |
      "## Поточні обмеження проєкту (Замороження Stage 6.0)
       - Stage 6.0 заморожено.
       - Не масштабуй Semantic Reconstruction...
       - Подальший прогрес... заблоковано до появи зовнішнього корпусу."

  - path: journal/0008-gretil-corpus-gate.yaml
    statement: "GRETIL корпус з проvenance acquired. 3951 сутр parsed. Cross-witness diff completed."

why_inconsistent: >
  Директива агента описує стан, який більше не актуальний.
  Корпус отримано (journal 0008), але правило агента не оновлено.
  Агент, який читає .agents/rules/epistemic_agent.md як перший документ,
  отримає хибну директиву.

epistemic_risk: >
  Якщо агент дотримується цього правила, він відмовиться від легітимної
  роботи з real corpus (L-001 testing), яку RESEARCH_MAP вже дозволяє.

recommended_resolution: >
  Оновити розділ "Поточні обмеження" в epistemic_agent.md.
  Замінити "Stage 6.0 заморожено" на опис актуального стану:
  Stage 6.0 trigger виконано (GRETIL corpus, journal 0008);
  L-001 (blind reconstruction) тепер дозволено на real corpus;
  синтетичні дані досі заборонені.

must_not_do:
  - Видалити історичну версію правила (зберегти в journal)
```

---

### ECA-003

```yaml
id: ECA-003
severity: medium
type: SUPERSESSION_MISSING
subject: phonological-dimensions-v0.2-not-superseded

files:
  - path: extensions/phonological-dimensions-v0.2.yaml
    statement: "status: draft (implied by absence of superseded field)"

  - path: extensions/phonological-dimensions-v0.3.yaml
    statement: |
      "status: reconciled
       reconciled_from:
         - phonological-dimensions-v0.2.yaml (sarvam agent, 4 levels)"

why_inconsistent: >
  v0.3 явно вказує, що reconciled from v0.2, але v0.2 не має поля
  status: superseded або superseded_by: phonological-dimensions-v0.3.yaml.
  Новий агент не знає, яка версія актуальна.

epistemic_risk: >
  Агент може використовувати v0.2 як поточну, ігноруючи reconciliation.

recommended_resolution: >
  Додати в v0.2:
    status: superseded
    superseded_by: phonological-dimensions-v0.3.yaml
    superseded_reason: "Reconciled with blind agent model in RECON-001"

must_not_do:
  - Видалити v0.2
  - Переписати v0.2 так, ніби вона завжди була v0.3
```

---

### ECA-004

```yaml
id: ECA-004
severity: medium
type: SUPERSESSION_MISSING
subject: claims-export-revision-stale

files:
  - path: docs/claims-export.yaml
    statement: "Revision baseline: a8391c41617331458e816698e5778971665f8436 (2026-08-15)"

  - path: repository state
    statement: "Current master: 636af77e2389 (2026-08-16)"

why_inconsistent: >
  Claims-export фіксує revision baseline на коміті a8391c4, але з того часу
  відбулися коміти: reconciliation report, v0.3 dimensions, UPC-8 prototype,
  документація. Claims-export не оновлено.
  Нові claims (H-SS-EXT-001..003, RECON-001 results) не експортовані.

epistemic_risk: >
  Downstream-споживач, який імпортує claims за revision a8391c4,
  не отримає результатів reconciliation ні sarvam claims.
  Якщо H-SS-EXT-001 стає STRENGTHENED, downstream не дізнається.

recommended_resolution: >
  Оновити claims-export.yaml:
  1. Додати H-SS-EXT-001, H-SS-EXT-002, H-SS-EXT-003 з актуальними статусами.
  2. Оновити revision baseline.
  3. Включити RECON-001 як evidence для H-SS-EXT-001.

must_not_do:
  - Видалити старі revision записи (зберегти історію)
```

---

### ECA-005

```yaml
id: ECA-005
severity: high
type: SCOPE_LEAK
subject: upc8-prototype-not-marked-as-engineering-hypothesis

files:
  - path: prototype/README.md
    statement: "This prototype implements the encoding/hardware layer of the five-layer architecture."

  - path: prototype/upc8.py
    statement: "No epistemic_layer or status field in code or comments."

  - path: docs/research_manifesto.md
    statement: |
      "XI. Śabda поки заморозити. Усі інженерні ідеї (Śabda-256, UPC-8)
       помістити в архів hypotheses/shabda/ зі статусом PREMATURE-HYPOTHESIS."
      "XII. І лише в самому кінці — машинне кодування."

  - path: hypotheses/shabda/status.yaml
    statement: "status: PREMATURE-HYPOTHESIS. H2: FPGA Hardware Acceleration (UPC-8)."

  - path: docs/epistemic-coordination.md
    statement: "Section 3: інженерні ідеї лишаються PREMATURE-HYPOTHESIS або ENGINEERING."

why_inconsistent: >
  Research manifesto каже: UPC-8 → hypotheses/shabda/, статус PREMATURE-HYPOTHESIS,
  тільки після завершення етапів I-XI.
  Epistemic coordination contract каже: інженерні ідеї → ENGINEERING або PREMATURE-HYPOTHESIS.
  Але prototype/ створений в корені репозиторію (не в hypotheses/shabda/),
  без статусу PREMATURE-HYPOTHESIS, без epistemic_layer: engineering.
  Причому L-001 (сліпа реконструкція) досі OPEN — тобто етапи I-XI не завершені.

epistemic_risk: >
  Новий агент може прочитати prototype/upc8.py як поточну інженерну
  реалізацію, а не як експеримент. Файл не містить жодного маркера,
  який каже "це гіпотеза, не факт" або "це engineering, не canonical".

recommended_resolution: >
  1. Додати в prototype/README.md та upc8.py:
     epistemic_layer: engineering
     status: experimental
     hypothesis_ref: hypotheses/shabda/status.yaml#H2
  2. Розрізнити "канонічна послідовність" (canon) та "канонічні коди 0x00-0x29"
     (engineering assignment) у кожній таблиці.

must_not_do:
  - Видалити prototype/ (це легітимний експеримент)
  - Підвищувати його статус до research claim
```

---

### ECA-006

```yaml
id: ECA-006
severity: medium
type: STATUS_INFLATION
subject: h-ss-ext-001-status-not-updated-after-reconciliation

files:
  - path: hypotheses/independent-claims-sarvam.yaml
    statement: "H-SS-EXT-001: status: HYPOTHESIS"

  - path: docs/reconciliation-sarvam-blind-001.md
    statement: "H-SS-EXT-001 (dimensions registry) — STRENGTHENED — 44 dimensions independently confirmed."

why_inconsistent: >
  Reconciliation report підвищив статус H-SS-EXT-001 з HYPOTHESIS до STRENGTHENED,
  але сам YAML файл не оновлено. "STRENGTHENED" не існує в словнику EPISTEMIC_CONTRACT.md
  (RESOLVED, REVIEWED, PROPOSED, UNRESOLVED-BY-EVIDENCE тощо).
  Твердження "44 dimensions independently confirmed" сильніше за HYPOTHESIS,
  але не має формального статусу в системі.

epistemic_risk: >
  Два джерела дають різний статус одному твердженню.
  Крім того, "STRENGTHENED" не є визначеним статусом — це інфляція
  словника епістемічних статусів без формального визначення.

recommended_resolution: >
  1. Визначити "STRENGTHENED" в EPISTEMIC_CONTRACT.md або
     замінити на існуючий статус (наприклад, SUPPORTED з evidence: RECON-001).
  2. Оновити independent-claims-sarvam.yaml: status: SUPPORTED
     з посиланням на reconciliation report як evidence.

must_not_do:
  - Видалити HYPOTHESIS з історії (додати supersedes, не переписувати)
```

---

### ECA-007

```yaml
id: ECA-007
severity: high
type: TERM_OVERLOAD
subject: canonical

files_using_term:
  - path: docs/epistemic-coordination.md
    usage: "канон 14 сутр (CANON) — переданий текст"
    meaning: traditional_canon

  - path: prototype/upc8.py
    usage: "canonical_space: range 0x00-0x29, policy: immutable"
    meaning: engineering_code_assignment

  - path: docs/claims-export.yaml
    usage: "SS-CANON-001: Канонічна послідовність 14 сутр"
    meaning: transmitted_text_with_provenance

  - path: docs/research-index.md
    usage: "Канонічна структура (Class B) єдино можлива"
    meaning: mathematically_proven_optimal_structure

  - path: extensions/phonological-dimensions-v0.3.yaml
    usage: "canonical_unit references (SS-XX:Y)"
    meaning: position_in_siva_sutra_sequence

why_inconsistent: >
  Слово "canonical" має щонайменше 5 різних значень:
  (1) переданий текст (традиційний канон)
  (2) числовий код 0x00-0x29 (engineering assignment)
  (3) текст з provenance (claims-export)
  (4) математично доведена оптимальна структура (research-index)
  (5) посилання на позицію в Шіва-сутрах (extensions)

  Формально статуси не конфліктують, але для агента це небезпечна полісемія.
  "Canonical code 0x09" не означає "канонічне число Паніні",
  але ніде це явно не розрізнено.

epistemic_risk: >
  Агент може змішати: "canonical code is immutable" (engineering decision)
  з "canonical sequence is immutable" (epistemic claim про переданий текст).
  Або: "SS-CANON-001 status RESOLVED" (текст з provenance)
  з "canonical structure is PROVED" (математичний доказ).

recommended_resolution: >
  Ввести явні префікси або qualified names:
  - canon:transmitted (переданий текст)
  - canon:code (engineering assignment)
  - canon:structure (mathematical property)
  - canon:ref (positional reference SS-XX:Y)
  Додати глосарій термінів у EPISTEMIC_CONTRACT.md або окремий файл.
```

---

### ECA-008

```yaml
id: ECA-008
severity: high
type: TERM_OVERLOAD
subject: provenance

files_using_term:
  - path: ksetra/EPISTEMIC_CONTRACT.md
    usage: "Provenance/Authenticity — історичне походження джерела"
    meaning: source_provenance (звідки походять дані)

  - path: extensions/phonological-dimensions-v0.3.yaml
    usage: "provenance: both-agree | sarvam | blind-agent | reconciled | disputed"
    meaning: inference_provenance (хто зробив висновок)

  - path: docs/claims-export.yaml
    usage: "provenance зафіксовано; текст узгоджено з традиційним каноном"
    meaning: source_provenance

  - path: hypotheses/independent-claims-sarvam.yaml
    usage: "Provenance: agent: sarvam-ai, repository_accessed: juv4uk/shiva-sutras"
    meaning: inference_provenance

why_inconsistent: >
  Дві ортогональні осі змішані в одному терміні:
  (a) evidence_provenance — звідки походять фонологічні дані (Whitney, Allen, GRETIL)
  (b) inference_provenance — хто зробив висновок (sarvam, blind-agent, reconciled)
  В v0.3 dimensions provenance = inference_provenance,
  в EPISTEMIC_CONTRACT provenance = source_provenance.
  Це не стилістична проблема — це онтологічна: один і той самий висновок
  може мати надійне джерело даних, але сумнівну інференцію, і навпаки.

epistemic_risk: >
  Агент, який читає provenance: both-agree в v0.3, може подумати,
  що це означає "джерело даних підтверджено обома агентами".
  Насправді це означає "обидва агенти класифікували цей вимір однаково" —
  що не каже нічого про надійність самих даних.

recommended_resolution: >
  Розділити:
  - evidence_provenance: Whitney/Allen/GRETIL/Vakulenko/...
  - inference_provenance: sarvam/blind-agent/reconciled/disputed
  Не використовувати голе слово "provenance" без кваліфікатора.
```

---

### ECA-009

```yaml
id: ECA-009
severity: medium
type: TERM_OVERLOAD
subject: resolved

files_using_term:
  - path: ksetra/EPISTEMIC_CONTRACT.md
    usage: "RESOLVED — операція і класи повністю і недвозначно доведені текстом джерела"
    meaning: textually_proven

  - path: RESEARCH_MAP.md
    usage: "Доступний незалежний корпус (Provenance) — RESOLVED"
    meaning: available_with_provenance

  - path: docs/claims-export.yaml
    usage: "SS-CANON-001 status: RESOLVED (provenance зафіксовано)"
    meaning: provenance_established

why_inconsistent: >
  RESOLVED має різну строгість:
  - В EPISTEMIC_CONTRACT: "недвозначно доведено текстом" — дуже висока планка.
  - В RESEARCH_MAP для L-002: "доступний з provenance" — нижча планка
    (наявність ≠ доведеність текстом).
  - В claims-export для SS-CANON-001: "provenance зафіксовано, текст узгоджено" —
    середня планка.

epistemic_risk: >
  Агент може застосувати строгість EPISTEMIC_CONTRACT до claims-export,
  або навпаки — послабити вимоги до pipeline statuses.

recommended_resolution: >
  Або уніфікувати визначення RESOLVED, або ввести підтипи:
  - RESOLVED-BY-TEXT (недвозначно доведено текстом)
  - RESOLVED-BY-PROVENANCE (джерело атрибутовано)
  - RESOLVED-BY-MODEL (доведено в моделі)
```

---

### ECA-010

```yaml
id: ECA-010
severity: medium
type: AUTHORITATIVE_SOURCE_AMBIGUITY
subject: multiple-language-registry-variants

files:
  - path: extensions/english.yaml
  - path: extensions/english-sarvam.yaml
  - path: extensions/english-kimi.yaml
  - path: extensions/ukrainian.yaml
  - path: extensions/ukrainian-sarvam.yaml
  - path: extensions/ukrainian-kimi.yaml

why_inconsistent: >
  Існує 3 варіанти англійської та 3 варіанти української реєстрів.
  Жоден документ не вказує, який є authoritative/current.
  Немає supersedes/superseded_by зв'язків між ними.

epistemic_risk: >
  Агент не знає, який реєстр використовувати для порівняння.
  Різні реєстри можуть давати різні результати.

recommended_resolution: >
  1. Позначити неактуальні варіанти як superseded.
  2. Або перейменувати: english.yaml → english-current.yaml,
     english-sarvam.yaml → english-agent-sarvam.yaml (archived).
  3. Додати README в extensions/, який вказує поточну версію.
```

---

### ECA-011

```yaml
id: ECA-011
severity: medium
type: PROVENANCE_AMBIGUITY
subject: blind-agent-model-not-persisted

files:
  - path: docs/reconciliation-sarvam-blind-001.md
    statement: |
      "Blind agent's model: not persisted (sub-agent sandbox was ephemeral);
       analysis preserved in this document."

  - path: extensions/phonological-dimensions-v0.3.yaml
    statement: "reconciled_from: blind-dimensions.yaml (blind agent, 6 levels, RECON-001)"

why_inconsistent: >
  v0.3 стверджує, що reconciled from blind-dimensions.yaml,
  але цей файл не існує в репозиторії.
  Сліпий експеримент не можна відтворити — сліпий агент не залишив артефакта.
  Є лише prose-опис в reconciliation report.
  Це порушує власний критерій успіху репозиторію:
  "Майбутній дослідник повинен мати змогу повністю відтворити логіку дослідження,
  використовуючи лише журнал, RESEARCH_MAP, експерименти та артефакти доказів."

epistemic_risk: >
  Без persistable артефакта blind experiment є анекдотою, не протоколом.
  "Blind agent був сліпим" — це твердження без перевірки.
  Не збережено: SHA файлів, переданих агенту; список файлів, яких він не бачив;
  prompt hash; модель/agent identifier; timestamp.

recommended_resolution: >
  1. Створити experiments/blind_reconstruction/recon-001/ директорію.
  2. Зберегти: input data (3 registries), prompt, output (blind agent's model),
     manifest (SHA, timestamp, model ID).
  3. Або, якщо відтворення неможливе, явно позначити RECON-001 як
     status: non-reproducible з причиною.
```

---

### ECA-012

```yaml
id: ECA-012
severity: low
type: STATUS_LAG
subject: research-index-section-4-frozen-status

files:
  - path: docs/research-index.md
    statement: "Розділ 4: Статус 🟡 ЗАВЕРШЕНО (Заморожено) — Створено чистий пул кандидатів для сліпої реконструкції (Stage 6.0)."

  - path: RESEARCH_MAP.md
    statement: "L-002 RESOLVED — корпус доступний."

why_inconsistent: >
  Research-index розділ 4 посилається на "Заморожено" як на поточний статус,
  хоча контекст змінився (Stage 6.0 trigger виконано).
  Це не пряма суперечність (розділ 4 описує етап candidate harvesting,
  а не Stage 6.0 freeze), але формулювання "Заморожено" вводить в оману.

epistemic_risk: >
  Низький. Агент може сплутати "candidate harvesting завершено і заморожено"
  з "Stage 6.0 заморожено".

recommended_resolution: >
  Уточнити формулювання: "Статус: ЗАВЕРШЕНО. Кандидати збережено.
  Stage 6.0 freeze стан — див. FREEZE_STAGE_6_0.md / STAGE_6_1_ACTIVATION.md."
```

---

### ECA-013

```yaml
id: ECA-013
severity: low
type: STATUS_INFLATION
subject: v03-commit-message-overclaim

files:
  - path: extensions/phonological-dimensions-v0.3.yaml
    statement: "status: reconciled"

  - path: git commit message (implied by user report)
    statement: "This ontology survived independent verification."

why_inconsistent: >
  Commit message формулює сильніше твердження, ніж підтримує evidence.
  44 dimensions отримали сильне незалежне підтвердження (RECON-001),
  але v0.3 reconciled класифікація — це синтез, не незалежно перевірена модель.
  "Survived independent verification" застосовано до всієї онтології,
  тоді як незалежно перевірено лише dimension extraction, не 6-level classification.

epistemic_risk: >
  Низький (commit message не є machine-readable), але створює прецедент
  інтерпретації v0.3 як "verified", а не "synthesized".

recommended_resolution: >
  Розрізнити в v0.3 header:
  - 44 dimensions: independently_confirmed (RECON-001)
  - 6-level classification: synthesized (not yet independently reproduced)
```

---

### ECA-014

```yaml
id: ECA-014
severity: medium
type: HISTORY_MUTATION_RISK
subject: journal-07-vs-journal-0008-sequencing

files:
  - path: journal/07_epistemic_rearming.md
    statement: "We did NOT unfreeze Stage 6.0. State: FROZEN -> ARMED / WAITING_FOR_CORPUS."
    date: 2026-08-15

  - path: journal/0008-gretil-corpus-gate.yaml
    statement: "GRETIL corpus acquired. status: EVIDENCE-LOGGED."
    date: 2026-08-15

why_inconsistent: >
  Обидва записи датовані 2026-08-15. Journal 07 каже "not unfrozen",
  journal 0008 фіксує виконання тригера.
  Неясна послідовність: чи 07 перед 0008, чи навпаки?
  Якщо 07 перед 0008 — то стан змінився, але не зафіксовано transition.
  Якщо 0008 перед 07 — то 07 містить застаріле твердження.

epistemic_risk: >
  Спокуса переписати journal 07, щоб він відображав post-0008 стан.
  Це порушило б append-only principle.

recommended_resolution: >
  Не переписувати journal 07. Замість цього:
  1. Створити journal/0009-stage-6-1-activation.yaml, який явно фіксує:
     "Journal 07 described state BEFORE corpus acquisition.
      Journal 0008 records corpus acquisition.
      This entry records the transition: ARMED -> ACTIVE."
  2. Заборонити видалення або зміну journal 07.
```

---

## Current Authority Graph

Граф показує, який документ є актуальним авторитетом для кожного типу інформації.
Документи, які не відмічені як superseded, вважаються поточними.

```
RESEARCH_MAP.md
   │
   ├── current claim status (table)
   │     ↑ authority for: епістемічні статуси ключових тверджень
   │
   ├── points to → docs/claims-export.yaml
   │     ↑ authority for: експортовані claims (downstream API)
   │     ⚠ revision baseline stale (ECA-004)
   │     ⚠ missing H-SS-EXT-001..003 (ECA-004)
   │
   ├── points to → docs/research-index.md
   │     ↑ authority for: історія експериментів
   │     ⚠ section 4 "Заморожено" stale (ECA-012)
   │
   └── points to → journal/
         │
         ├── journal/07_epistemic_rearming.md
         │     ↑ HISTORICAL: описує стан до corpus acquisition
         │     ⚠ не позначений як superseded (ECA-014)
         │
         └── journal/0008-gretil-corpus-gate.yaml
               ↑ CURRENT: фіксує acquisition GRETIL corpus
               ↑ але не створено UNFREEZE документа (ECA-001)

FREEZE_STAGE_6_0.md
   │
   ├── status: frozen (як написано)
   │     ⚠ SUPERSEDED by evidence in journal/0008 (ECA-001)
   │     ⚠ але не позначений superseded
   │
   └── frozen_commit: "TBD"
         ⚠ ніколи не заповнено

.agents/rules/epistemic_agent.md
   │
   ├── OPERATIONAL: правила агента
   │     ⚠ STALE: "Stage 6.0 заморожено" (ECA-002)
   │
   └── points to → docs/epistemic-coordination.md
         ↑ CURRENT: контракт координації

ksetra/EPISTEMIC_CONTRACT.md
   │
   └── CONSTITUTION: епістемічні статуси та аксіоми
         ⚠ TERM_OVERLOAD: "resolved", "provenance" (ECA-008, ECA-009)

extensions/
   │
   ├── phonological-dimensions-v0.3.yaml
   │     ↑ CURRENT: reconciled dimension registry
   │
   ├── phonological-dimensions-v0.2.yaml
   │     ⚠ SUPERSEDED by v0.3, але не позначений (ECA-003)
   │
   ├── english.yaml / english-sarvam.yaml / english-kimi.yaml
   │     ⚠ AMBIGUOUS: який authoritative? (ECA-010)
   │
   └── ukrainian.yaml / ukrainian-sarvam.yaml / ukrainian-kimi.yaml
         ⚠ AMBIGUOUS: який authoritative? (ECA-010)

hypotheses/
   │
   ├── independent-claims-sarvam.yaml
   │     ⚠ H-SS-EXT-001 status stale: HYPOTHESIS → should be SUPPORTED (ECA-006)
   │
   └── shabda/status.yaml
         ↑ CURRENT: PREMATURE-HYPOTHESIS для UPC-8
         ⚠ prototype/ не посилається на цей файл (ECA-005)

prototype/
   │
   ├── upc8.py
   │     ⚠ no epistemic_layer: engineering marker (ECA-005)
   │     ⚠ no status: experimental marker (ECA-005)
   │
   ├── test_upc8.py
   │
   ├── README.md
   │     ⚠ claims "encoding/hardware layer" without PREMATURE-HYPOTHESIS (ECA-005)
   │
   └── UPC8-documentation-ua.md
```

---

## Навігаційна ясність

**Питання:** Чи може новий агент, читаючи репозиторій у рекомендованому порядку (README → RESEARCH_MAP → freeze → agent rules), однозначно визначити актуальний стан?

**Відповідь:** Ні. Послідовність читання:

```
README.md
  → "Почніть з RESEARCH_MAP" ✓
RESEARCH_MAP.md
  → "L-002 RESOLVED, корпус доступний" ✓
  → Але далі агент читає:
FREEZE_STAGE_6_0.md
  → "Stage 6.0 frozen" ✗ (суперечить RESEARCH_MAP)
.agents/rules/epistemic_agent.md
  → "Stage 6.0 заморожено" ✗ (підтримує freeze, суперечить RESEARCH_MAP)
```

Агент стикається з протиріччям на кроці 3 і не має документа, який би
однозначно вирішив, який стан актуальний. Journal 0008 фіксує evidence,
але не створює формального transition document.

---

## Підсумок

| ID | Severity | Type | Subject |
|---|---|---|---|
| ECA-001 | high | STATE_CONTRADICTION | Stage 6.0 freeze vs RESOLVED |
| ECA-002 | high | STALE_DIRECTIVE | Agent rule says frozen, corpus resolved |
| ECA-003 | medium | SUPERSESSION_MISSING | v0.2 not marked superseded by v0.3 |
| ECA-004 | medium | SUPERSESSION_MISSING | claims-export revision stale, missing H-SS-EXT claims |
| ECA-005 | high | SCOPE_LEAK | UPC-8 prototype not marked as engineering/premature |
| ECA-006 | medium | STATUS_INFLATION | H-SS-EXT-001 status not updated after RECON-001 |
| ECA-007 | high | TERM_OVERLOAD | "canonical" — 5 різних значень |
| ECA-008 | high | TERM_OVERLOAD | "provenance" — source vs inference змішані |
| ECA-009 | medium | TERM_OVERLOAD | "resolved" — різна строгість |
| ECA-010 | medium | AUTHORITATIVE_SOURCE_AMBIGUITY | 3 варіанти english/ukrainian YAML, який поточний? |
| ECA-011 | medium | PROVENANCE_AMBIGUITY | Blind agent model not persisted, experiment non-reproducible |
| ECA-012 | low | STATUS_LAG | Research-index section 4 "Заморожено" misleading |
| ECA-013 | low | STATUS_INFLATION | v0.3 commit message overclaims "survived verification" |
| ECA-014 | medium | HISTORY_MUTATION_RISK | Journal 07 vs 0008 sequencing unclear |

**Всього:** 14 знахідок  
**High:** 5  
**Medium:** 7  
**Low:** 2  

---

## Принципи аудиту

- Цей документ лише фіксує проблеми. Remediation — окремими комітами після review.
- Жодна рекомендація не вимагає видалення або переписування історії.
- Усі рекомендації використовують append-only / supersedes механізм.
- Аудит не модифікував жодного файлу в репозиторії.

---

*Агент: sarvam-ai (зовнішній діагностичний аудит, без модифікації репозиторію)*  
*Commit: 636af77e23895ed121fcb7bc72c5b64f2755f648*  
*Дата: 2026-08-16*