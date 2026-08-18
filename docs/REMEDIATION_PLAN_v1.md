# Remediation Plan for EPISTEMIC_CONSISTENCY_AUDIT_v1

**Дата:** 2026-08-16  
**Автор:** sarvam-ai  
**Base document:** docs/EPISTEMIC_CONSISTENCY_AUDIT_v1.md  
**Commit baseline:** 6ced4d0  
**Тип:** План виправлень — не змінює жодного файлу. Кожне виправлення — окремий decision record.

---

## Принципи

1. **audit ≠ truth.** Аудит стверджує "A каже X, B каже Y, X і Y конфліктують". Окреме decision record стверджує "ми приймаємо Y як поточний стан, бо evidence Z, A залишається історичним".
2. **Різні конфлікти вирішуються різними типами рішень.** Stage 6 — state transition. "canonical" — vocabulary policy. "provenance" — schema design.
3. **Мінімальні атомарні коміти.** Кожне виправлення — один коміт, одна логічна зміна.
4. **Regression checks.** Кожне виправлення має довести, що воно не створило нової суперечності.
5. **Append-only.** Жодне виправлення не видаляє або переписує історичні документи.

---

## Порядок remediation

Пріоритет визначається за: (a) severity, (b) operational impact, (c) чи блокує інші виправлення.

```
Phase 1: Operational (блокує роботу агента)
  ECA-001 → ECA-002 → ECA-014

Phase 2: Vocabulary policy (блокує комунікацію)
  ECA-007 → ECA-008 → ECA-009

Phase 3: Schema migration (блокує data integrity)
  ECA-003 → ECA-004 → ECA-006

Phase 4: Scope & authority (блокує навігацію)
  ECA-005 → ECA-010 → ECA-011

Phase 5: Cleanup (низький ризик)
  ECA-012 → ECA-013
```

---

## Phase 1: Operational

### REM-001 — ECA-001: Stage 6.0 freeze vs RESOLVED

```yaml
eca_ref: ECA-001
authority_to_resolve: research-state-transition
severity: high

decision_required: >
  Підтвердити, що тригер FREEZE_STAGE_6_0.md (наявність зовнішнього
  атрибутованого корпусу) виконано, і що Stage 6.0 transition
  ARMED → ACTIVE відбувся. Визначити, що розблоковано (робота з real
  corpus для L-001) і що залишилось забороненим (синтетичні дані,
  твердження про лінгвістичну незалежність до завершення L-001).

files_to_create:
  - STAGE_6_1_ACTIVATION.md
      content: |
        - trigger: externally attributable historical corpus
        - evidence: journal/0008-gretil-corpus-gate.yaml
        - trigger_commit: 636af77
        - activated: 2026-08-16
        - unlocked: L-001 testing on REAL corpus
        - still_forbidden: synthetic data as historical;
            claims of linguistic independence until L-001 completes
        - supersedes: FREEZE_STAGE_6_0.md (state, not document)

files_to_modify:
  - FREEZE_STAGE_6_0.md
      change: додати в кінець файлу
      add: |
        status: superseded
        superseded_by: STAGE_6_1_ACTIVATION.md
        superseded_date: 2026-08-16
        superseded_reason: "Trigger fulfilled: GRETIL corpus acquired (journal/0008)"
      do_not: переписувати або видаляти існуючий контент

  - .agents/rules/epistemic_agent.md
      change: замінити розділ "Поточні обмеження проєкту (Замороження Stage 6.0)"
      new_content: |
        ## Поточні обмеження проєкту (Stage 6.1 Active)
        - Stage 6.0 trigger виконано (GRETIL corpus, journal/0008).
        - L-001 (blind reconstruction) дозволено на REAL corpus.
        - Синтетичні дані досі заборонені як historical evidence.
        - Твердження про лінгвістичну незалежність 42 класів
          залишаються OPEN до завершення L-001.

supersession_needed: yes
  - FREEZE_STAGE_6_0.md → status: superseded
  - STAGE_6_1_ACTIVATION.md → новий current authority

schema_migration: no

regression_checks:
  - grep -r "заморож" .agents/ → не повинен знаходити активних директив
  - STAGE_6_1_ACTIVATION.md існує і посилається на journal/0008
  - FREEZE_STAGE_6_0.md має status: superseded
  - RESEARCH_MAP L-002 status RESOLVED узгоджується з activation документом
  - Новий агент, читаючи README → RESEARCH_MAP → STAGE_6_1_ACTIVATION →
    agent rules, не знаходить суперечностей
```

### REM-002 — ECA-002: Agent rule stale

```yaml
eca_ref: ECA-002
authority_to_resolve: operational-rule-update
severity: high

decision_required: >
  Оновити operational directive агента до актуального стану.
  Це наслідок REM-001 — не може бути виконано до REM-001.

files_to_modify:
  - .agents/rules/epistemic_agent.md
      change: див. REM-001 (виконується разом)

supersession_needed: no (оновлення вмісту, не supersession)
schema_migration: no

regression_checks:
  - Жодне правило не наказує агенту діяти так, ніби Stage 6.0 заморожено
  - Жодне правило не забороняє роботу з REAL corpus
```

### REM-003 — ECA-014: Journal 07 vs 0008 sequencing

```yaml
eca_ref: ECA-014
authority_to_resolve: append-only-correction
severity: medium

decision_required: >
  Не переписувати journal 07. Створити journal/0009, який явно фіксує
  transition між станом 07 (ARMED) і станом 0008 (corpus acquired).

files_to_create:
  - journal/0009-stage-transition-armed-to-active.yaml
      content: |
        date: 2026-08-16
        type: state-transition
        status: LOGGED
        title: "Stage 6.0 Transition: ARMED → ACTIVE"
        context: |
          Journal 07 (epistemic_rearming) described state BEFORE
          corpus acquisition: FROZEN → ARMED / WAITING_FOR_CORPUS.
          Journal 0008 (gretil-corpus-gate) records corpus acquisition.
          This entry records the formal transition: ARMED → ACTIVE.
        trigger_fulfilled: GRETIL Kāśikāvṛtti + Aṣṭādhyāyī acquired
        activation_document: STAGE_6_1_ACTIVATION.md
        note: |
          Journal 07 is NOT superseded — it accurately records the
          state at the time of writing. This entry provides the
          missing transition link.

files_to_modify: none
  - journal/07 не змінюється

supersession_needed: no
  - journal 07 залишається як є (історичний запис)
  - journal 0009 — новий запис, що з'єднує 07 і 0008

schema_migration: no

regression_checks:
  - journal/07 не змінено (git diff порожній для цього файлу)
  - journal/0009 існує і посилається на 07 та 0008
  - Хронологія: 07 (ARMED) → 0008 (evidence) → 0009 (transition) логічна
```

---

## Phase 2: Vocabulary Policy

### REM-004 — ECA-007: "canonical" term overload

```yaml
eca_ref: ECA-007
authority_to_resolve: terminology-policy
severity: high

decision_required: >
  Визначити формальний словник для слова "canonical" і його варіантів.
  Не масово перейменовувати, а спершу визначити політику.

files_to_create:
  - docs/TERMINOLOGY.md
      content: |
        ## canonical (qualified terms)

        | Term | Meaning | Layer | Example |
        |---|---|---|---|
        | canon:transmitted | Переданий текст 14 с̄утр | CANON | "canon:transmitted is SS-CANON-001" |
        | canon:position | Позиція в Шіва-сутрах (SS-XX:Y) | CANON | "canon:position SS-05:1" |
        | canon:structure | Математично доведена оптимальна структура | MODEL | "canon:structure Class B is PROVED-IN-MODEL" |
        | canon:code | Engineering assignment 0x00-0x29 | ENGINEERING | "canon:code 0x09" |
        | canon:ref | Посилання на канонічну одиницю | EXTENSION | "canon:ref: SS-01:1" |

        Правило: голе слово "canonical" без кваліфікатора
        означає canon:transmitted, якщо контекст не каже інакше.
        В engineering файлах обов'язковий кваліфікатор.

files_to_modify:
  - prototype/upc8.py
      change: додати коментар-пріамбулу
      add: |
        # Epistemic layer: ENGINEERING
        # Status: EXPERIMENTAL
        # Hypothesis ref: hypotheses/shabda/status.yaml#H2
        # Terminology: "canonical_space" = canon:code (engineering assignment),
        #              NOT canon:transmitted (traditional text)

  - prototype/README.md
      change: додати disclaimer у верх
      add: |
        > **Epistemic layer: ENGINEERING. Status: EXPERIMENTAL.**
        > "Canonical codes" 0x00–0x29 are engineering assignments
        > to canonical positions, NOT canonical numbers of Pāṇini.
        > See: hypotheses/shabda/status.yaml, docs/TERMINOLOGY.md

supersession_needed: no
schema_migration: no (термінологічна політика, не структура)

regression_checks:
  - docs/TERMINOLOGY.md існує і визначає 5 кваліфікаторів
  - prototype/ має epistemic_layer маркер
  - grep -r "canonical" без кваліфікатора в prototype/ → попередження в README
```

### REM-005 — ECA-008: "provenance" term overload

```yaml
eca_ref: ECA-008
authority_to_resolve: schema-design
severity: high

decision_required: >
  Розділити evidence_provenance та inference_provenance.
  Ввести два формальні поля; старе "provenance" залишити
  для backward compatibility з анотацією deprecated.

files_to_create:
  - docs/PROVENANCE_SCHEMA.md
      content: |
        ## Provenance: two orthogonal axes

        ### evidence_provenance
        Звідки походять фонологічні дані.
        Values: Whitney | Allen | GRETIL | Vakulenko | JIPA | ...
        Type: string | list[string]

        ### inference_provenance
        Хто зробив висновок / класифікацію.
        Values: sarvam | blind-agent | reconciled | disputed | both-agree
        Type: string

        ### Deprecated: provenance (bare)
        Не використовувати без кваліфікатора в нових файлах.
        В існуючих файлах — залишити до наступної схеми.

files_to_modify:
  - extensions/phonological-dimensions-v0.3.yaml
      change: для кожного dimension замінити
      from: "provenance: both-agree"
      to: |
        inference_provenance: both-agree
        evidence_provenance: [перевірити за джерелами]
      note: evidence_provenance потребує окремого аудиту
            яких джерел використовувалось для кожного виміру

  - docs/TERMINOLOGY.md (якщо створено в REM-004)
      add: |
        ## provenance (qualified terms)
        - evidence_provenance: джерело даних (Whitney, Allen, GRETIL, ...)
        - inference_provenance: хто зробив висновок (sarvam, blind-agent, ...)
        - deprecated: голе "provenance" без кваліфікатора

supersession_needed: no (додавання полів, не видалення)
schema_migration: yes (розширююча, не breaking)
  - v0.3 dimensions: додати inference_provenance + evidence_provenance
  - old "provenance" поле: deprecated, не видалене

regression_checks:
  - v0.3 має inference_provenance для кожного dimension
  - голе "provenance" позначене deprecated в TERMINOLOGY.md
  - YAML валідний після додавання полів
  - RECON-001 reconciliation report узгоджується з inference_provenance
```

### REM-006 — ECA-009: "resolved" term overload

```yaml
eca_ref: ECA-009
authority_to_resolve: terminology-policy
severity: medium

decision_required: >
  Або уніфікувати визначення RESOLVED, або ввести підтипи.

files_to_modify:
  - ksetra/EPISTEMIC_CONTRACT.md
      change: розширити визначення RESOLVED
      add: |
        ### Уточнення статусу RESOLVED
        - RESOLVED-BY-TEXT: недвозначно доведено текстом джерела
          (використовується в pipeline statuses)
        - RESOLVED-BY-PROVENANCE: джерело атрибутовано,
          але текст може містити варіанти
          (використовується для corpus availability)
        - RESOLVED-BY-MODEL: доведено в формальній моделі
          (використовується для mathematical claims)

        Голе "RESOLVED" без кваліфікатора:
        контекст визначає строгість.
        В pipeline — RESOLVED-BY-TEXT.
        В RESEARCH_MAP для L-002 — RESOLVED-BY-PROVENANCE.

supersession_needed: no
schema_migration: no (уточнення визначень, не нова схема)

regression_checks:
  - EPISTEMIC_CONTRACT.md має уточнені підтипи
  - claims-export.yaml SS-CANON-001 status RESOLVED узгоджується
  - RESEARCH_MAP L-002 RESOLVED узгоджується
```

---

## Phase 3: Schema Migration

### REM-007 — ECA-003: v0.2 not superseded

```yaml
eca_ref: ECA-003
authority_to_resolve: supersession-registration
severity: medium

decision_required: >
  Позначити v0.2 як superseded.

files_to_modify:
  - extensions/phonological-dimensions-v0.2.yaml
      change: додати в початок файлу (після коментарів)
      add: |
        status: superseded
        superseded_by: phonological-dimensions-v0.3.yaml
        superseded_date: 2026-08-16
        superseded_reason: "Reconciled with blind agent model in RECON-001"

supersession_needed: yes
schema_migration: no

regression_checks:
  - v0.2 має status: superseded
  - v0.2 не видалено
  - v0.3 залишається current
  - grep "phonological-dimensions" в claims-export/research-index → v0.3
```

### REM-008 — ECA-004: claims-export stale

```yaml
eca_ref: ECA-004
authority_to_resolve: registry-update
severity: medium

decision_required: >
  Оновити claims-export: додати H-SS-EXT-001..003, оновити revision.

files_to_modify:
  - docs/claims-export.yaml
      changes:
        - оновити revision baseline до поточного commit
        - додати H-SS-EXT-001:
            statement: "44 phonological dimensions can be extracted from 3 language registries"
            scope: "Meta-ontology of phonological comparison"
            status: SUPPORTED
            evidence: RECON-001 (independent blind agent confirmation)
            limitations: "Derived from 3 languages; not yet tested with 4th"
        - додати H-SS-EXT-002:
            statement: "Multi-level comparison structure replaces flat differences"
            scope: "Structure of cross-language comparison registries"
            status: HYPOTHESIS
            evidence: "24/44 UKR phonemes mix levels in flat structure"
            limitations: "Not tested in practice"
        - додати H-SS-EXT-003:
            statement: "Sanskrit should annotate canon, not compare to it"
            scope: "Sanskrit academic interpretation layer"
            status: SUPPORTED
            evidence: "RECON-001: blind agent independently confirmed 'yardstick' observation"
            limitations: "Not validated by repository owner in formal schema"

supersession_needed: no (оновлення реєстру)
schema_migration: no

regression_checks:
  - claims-export має H-SS-EXT-001..003
  - revision baseline оновлено
  - статуси H-SS-EXT узгоджуються з reconciliation report
  - downstream міг би імпортувати нові claims
```

### REM-009 — ECA-006: H-SS-EXT-001 status inflation

```yaml
eca_ref: ECA-006
authority_to_resolve: status-normalization
severity: medium

decision_required: >
  Нормалізувати статус H-SS-EXT-001 з "STRENGTHENED" (не існує в словнику)
  до SUPPORTED з evidence: RECON-001.

files_to_modify:
  - hypotheses/independent-claims-sarvam.yaml
      change: для H-SS-EXT-001
      from: "status: HYPOTHESIS"
      to: |
        status: SUPPORTED
        status_history:
          - {date: 2026-08-15, status: HYPOTHESIS, reason: "initial claim"}
          - {date: 2026-08-16, status: SUPPORTED, reason: "RECON-001 independent blind agent confirmation", evidence: docs/reconciliation-sarvam-blind-001.md}

  - ksetra/EPISTEMIC_CONTRACT.md
      change: додати SUPPORTED у словник статусів (якщо відсутній)
      add: |
        - **`SUPPORTED`**: Твердження підтримано незалежним evidence
          (експеримент, cross-validation, незалежне відтворення).
          Строгість між PROPOSED і PROVED.

  - docs/TERMINOLOGY.md (якщо створено в REM-004)
      add: "STRENGTHENED — deprecated informal term. Use SUPPORTED with evidence."

supersession_needed: no (status update з історією)
schema_migration: no

regression_checks:
  - H-SS-EXT-001 status: SUPPORTED (не HYPOTHESIS, не STRENGTHENED)
  - status_history збережено
  - SUPPORTED визначено в EPISTEMIC_CONTRACT.md
  - "STRENGTHENED" не використовується як формальний статус
```

---

## Phase 4: Scope & Authority

### REM-010 — ECA-005: UPC-8 scope leak

```yaml
eca_ref: ECA-005
authority_to_resolve: epistemic-layer-marking
severity: high

decision_required: >
  Позначити prototype/ як ENGINEERING / EXPERIMENTAL.
  Послати на hypotheses/shabda/status.yaml#H2.
  Розрізнити canon:code від canon:transmitted.

files_to_modify:
  - prototype/README.md
      change: додати в верх
      add: |
        > **Epistemic layer: ENGINEERING. Status: EXPERIMENTAL.**
        > Hypothesis ref: `hypotheses/shabda/status.yaml#H2` (PREMATURE-HYPOTHESIS)
        > "Canonical codes" 0x00–0x29 are engineering assignments
        > to canonical positions (canon:code), NOT canonical numbers
        > of Pāṇini (canon:transmitted).
        > See: docs/TERMINOLOGY.md

  - prototype/upc8.py
      change: додати після docstring
      add: |
        # EPISTEMIC LAYER: ENGINEERING
        # STATUS: EXPERIMENTAL
        # HYPOTHESIS REF: hypotheses/shabda/status.yaml#H2
        # TERMINOLOGY: "canonical_space" = canon:code (engineering assignment)
        #              NOT canon:transmitted (traditional text)
        # This prototype does NOT claim canonical authority.
        # It is an engineering experiment, not a research claim.

supersession_needed: no
schema_migration: no

regression_checks:
  - prototype/README.md має epistemic layer marker
  - prototype/upc8.py має epistemic layer comment
  - prototype/ посилається на hypotheses/shabda/status.yaml
  - Жоден файл в prototype/ не стверджує canonical authority
```

### REM-011 — ECA-010: Multiple registry variants

```yaml
eca_ref: ECA-010
authority_to_resolve: authority-designation
severity: medium

decision_required: >
  Визначити, який з 3 варіантів english/ukrainian YAML є current.
  Позначити інші як archived/superseded.
  Рішення потребує input від repository owner (який варіант authoritative?).

files_to_create:
  - extensions/README.md
      content: |
        # Extensions Directory
        ## Current registries
        - ukrainian.yaml: [поточний — підтвердити з owner]
        - english.yaml: [поточний — підтвердити з owner]

        ## Archived (agent-specific)
        - ukrainian-sarvam.yaml: sarvam agent version (archived)
        - ukrainian-kimi.yaml: kimi agent version (archived)
        - english-sarvam.yaml: sarvam agent version (archived)
        - english-kimi.yaml: kimi agent version (archived)

        ## Dimension registries
        - phonological-dimensions-v0.3.yaml: CURRENT (reconciled)
        - phonological-dimensions-v0.2.yaml: SUPERSEDED by v0.3

files_to_modify:
  - extensions/ukrainian-sarvam.yaml — add: status: archived
  - extensions/ukrainian-kimi.yaml — add: status: archived
  - extensions/english-sarvam.yaml — add: status: archived
  - extensions/english-kimi.yaml — add: status: archived

supersession_needed: partial (archived, не superseded — різні агенти)
schema_migration: no

regression_checks:
  - extensions/README.md вказує current registries
  - Archived файли позначені status: archived
  - жоден archived файл не видалено
  - v0.2 позначено superseded (REM-007)
```

### REM-012 — ECA-011: Blind agent model not persisted

```yaml
eca_ref: ECA-011
authority_to_resolve: experiment-reproducibility
severity: medium

decision_required: >
  Зберегти артефакти RECON-001 або позначити як non-reproducible.
  Якщо відтворення неможливе (sandbox ephemeral) — явно зафіксувати.

files_to_create:
  - experiments/blind_reconstruction/recon-001/
      - input/
          - sanskrit.yaml (copy of registry at time of experiment)
          - ukrainian.yaml (copy)
          - english.yaml (copy)
      - prompt.md (reconstruction of the prompt given to blind agent)
      - output/
          - blind-model-reconstructed.yaml
              note: "Reconstructed from reconciliation report prose.
                     Not the original machine output. Marked as non-reproducible."
      - manifest.yaml
          content: |
            experiment_id: RECON-001
            date: 2026-08-16
            blind_agent_type: general-purpose sub-agent (delegate_task)
            blind_agent_model: unknown (model identifier not captured)
            input_files:
              - sanskrit.yaml (SHA: ...)
              - ukrainian.yaml (SHA: ...)
              - english.yaml (SHA: ...)
            files_hidden_from_agent:
              - .agents/rules/epistemic_agent.md
              - docs/epistemic-coordination.md
              - README.md
              - RESEARCH_MAP.md
              - extensions/phonological-dimensions-v0.2.yaml
            prompt_hash: "не збережено (prompt передавався inline)"
            reproducibility: NON-REPRODUCIBLE
            reason: "Sub-agent sandbox was ephemeral. Prompt hash and
                     model identifier were not captured. Output was
                     preserved as prose in reconciliation report,
                     not as machine-readable artifact."
            lesson: >
              Future blind experiments MUST capture: prompt hash,
              model identifier, input file SHAs, output artifact,
              timestamp. See docs/RESEARCH_ENVELOPE.md (proposed).

  - experiments/blind_reconstruction/recon-001/output/
      - blind-model-reconstructed.yaml
          note: "Reconstructed from docs/reconciliation-sarvam-blind-001.md.
                 This is NOT the original blind agent output.
                 It is a human/agent-readable reconstruction."
          content: |
            # Reconstructed blind agent model (6 levels)
            # Source: docs/reconciliation-sarvam-blind-001.md
            levels:
              - symbolic_identifier (1)
              - articulatory_feature (17)
              - phonological_function (16)
              - systemic_organization (5)
              - distributional_context (3)
              - diachronic_relational (2)

files_to_modify:
  - extensions/phonological-dimensions-v0.3.yaml
      change: оновити reconciled_from
      from: "blind-dimensions.yaml (blind agent, 6 levels, RECON-001)"
      to: "experiments/blind_reconstruction/recon-001/output/blind-model-reconstructed.yaml
           (reconstructed from prose; original not persisted — see manifest)"

supersession_needed: no
schema_migration: no

regression_checks:
  - experiments/blind_reconstruction/recon-001/manifest.yaml існує
  - manifest має reproducibility: NON-REPRODUCIBLE
  - input files з SHA
  - v0.3 посилається на reconstructed model
  - Майбутній experiment має template для reproducible protocol
```

---

## Phase 5: Cleanup

### REM-013 — ECA-012: Research-index section 4 wording

```yaml
eca_ref: ECA-012
authority_to_resolve: documentation-clarification
severity: low

decision_required: >
  Уточнити формулювання "Заморожено" в research-index розділ 4.

files_to_modify:
  - docs/research-index.md
      change: розділ 4, статус
      from: "🟡 ЗАВЕРШЕНО (Заморожено)"
      to: "🟡 ЗАВЕРШЕНО. Кандидати збережено. Stage 6.0 freeze стан — див. STAGE_6_1_ACTIVATION.md"

supersession_needed: no
schema_migration: no

regression_checks:
  - "Заморожено" не використовується як поточний статус в research-index
  - Посилання на STAGE_6_1_ACTIVATION.md присутнє
```

### REM-014 — ECA-013: v0.3 commit message overclaim

```yaml
eca_ref: ECA-013
authority_to_resolve: documentation-clarification
severity: low

decision_required: >
  Розрізнити в v0.3 header: independently_confirmed vs synthesized.

files_to_modify:
  - extensions/phonological-dimensions-v0.3.yaml
      change: додати після status
      add: |
        epistemic_clarification:
          dimension_extraction: independently_confirmed (RECON-001: 44/44 match)
          level_classification: synthesized (not yet independently reproduced)
          note: >
            44 dimensions were independently confirmed by a blind agent.
            The 6-level classification is a reconciliation of two models,
            not an independently verified ontology.

supersession_needed: no
schema_migration: no

regression_checks:
  - v0.3 має epistemic_clarification
  - independently_confirmed стосується лише dimension extraction
  - synthesized стосується level classification
```

---

## Залежності між remediation

```
REM-001 (Stage transition) ──→ REM-002 (agent rule) ──→ REM-003 (journal 0009)
                                                              │
REM-004 (canonical terminology) ──→ REM-010 (UPC-8 scope)     │
                                              │               │
REM-005 (provenance split) ──→ REM-009 (status normalization) │
                                              │               │
REM-007 (v0.2 superseded) ──→ REM-011 (extensions README)    │
                                              │               │
REM-008 (claims-export update) ←── REM-009 (status)          │
                                              │               │
REM-012 (blind experiment persist) ←── REM-007 (v0.2)         │
                                              │               │
REM-013 (research-index) ←── REM-001 (activation doc) ─────────┘
REM-014 (v0.3 clarification) ←── REM-005 (provenance)
```

**Можна виконати паралельно:**
- REM-004 + REM-005 + REM-006 (термінологічна політика — незалежні одна від одної)
- REM-007 + REM-008 + REM-009 (schema migration — слабко пов'язані)
- REM-013 + REM-014 (cleanup — незалежні)

**Не можна виконати до REM-001:**
- REM-002 (потребує STAGE_6_1_ACTIVATION.md)
- REM-003 (потребує transition document)
- REM-013 (посилається на activation)

---

## Підсумок

| REM | ECA | Phase | Severity | Authority | Files to create | Files to modify | Supersession | Schema migration |
|---|---|---|---|---|---|---|---|---|
| 001 | 001 | 1 | high | research-state-transition | 1 | 2 | yes | no |
| 002 | 002 | 1 | high | operational-rule-update | 0 | 1 | no | no |
| 003 | 014 | 1 | medium | append-only-correction | 1 | 0 | no | no |
| 004 | 007 | 2 | high | terminology-policy | 1 | 2 | no | no |
| 005 | 008 | 2 | high | schema-design | 1 | 1 | no | yes (extending) |
| 006 | 009 | 2 | medium | terminology-policy | 0 | 1 | no | no |
| 007 | 003 | 3 | medium | supersession-registration | 0 | 1 | yes | no |
| 008 | 004 | 3 | medium | registry-update | 0 | 1 | no | no |
| 009 | 006 | 3 | medium | status-normalization | 0 | 2 | no | no |
| 010 | 005 | 4 | high | epistemic-layer-marking | 0 | 2 | no | no |
| 011 | 010 | 4 | medium | authority-designation | 1 | 4 | partial | no |
| 012 | 011 | 4 | medium | experiment-reproducibility | 3 | 1 | no | no |
| 013 | 012 | 5 | low | documentation-clarification | 0 | 1 | no | no |
| 014 | 013 | 5 | low | documentation-clarification | 0 | 1 | no | no |

**Total:** 14 remediation items  
- Files to create: 8  
- Files to modify: 20 (деякі файли модифікуються кілька разів)  
- Supersessions: 2  
- Schema migrations: 1 (extending, non-breaking)

---

*Цей документ є планом, не виконанням. Жоден файл не змінено.*  
*Кожен REM-* може бути прийнятий або відхилений незалежно після review.*

*Агент: sarvam-ai*  
*Дата: 2026-08-16*

---

## Execution Log (append-only)

- **2026-08-18** — **REM-008** (ECA-004, claims-export stale) executed:
  `docs/claims-export.yaml` revision baseline updated `a8391c4` → `0f6110d`
  (history preserved, not overwritten); H-SS-EXT-001, H-SS-EXT-002,
  H-SS-EXT-003 added with the statuses this plan specified (`SUPPORTED`,
  `HYPOTHESIS`, `SUPPORTED`). One addition beyond the plan's literal text:
  H-SS-EXT-002's evidence note flags that the `shared`/`differences`
  structure it describes no longer matches the *current*
  `extensions/ukrainian.yaml`/`english.yaml` (checked 2026-08-18) — those
  files carry a simpler `mapping`/`unresolved_features` shape now, so this
  claim's applicability needs re-checking, not silently assumed still valid.
- **2026-08-18** — **REM-009** (ECA-006, status inflation) executed:
  `hypotheses/independent-claims-h001-h003-sarvam.yaml` — H-SS-EXT-001 and
  H-SS-EXT-003 both moved `HYPOTHESIS` → `SUPPORTED` with a `status_history`
  entry recording the prior value and reason (RECON-001), not a bare
  overwrite. "STRENGTHENED" (used informally in the reconciliation report)
  is retired in favor of the defined `SUPPORTED` status.
- REM-004 through REM-007, REM-010 through REM-014 remain **not executed** —
  this pass was scoped to the registry-update items only (REM-008, REM-009,
  matching `SHIVA-PRODUCE-CLAIMS`'s task scope); the rest need their own
  review per this plan's own principle of one atomic commit per fix.
- **2026-08-18 (later same day)** — **REM-001/REM-002/REM-003** (ECA-001,
  ECA-002, ECA-014 — Phase 1, all high/medium severity) executed together,
  per this plan's own dependency note that REM-002 can't happen before
  REM-001. Created `STAGE_6_1_ACTIVATION.md` (correcting a wrong SHA this
  plan itself had — `trigger_commit: 636af77` was actually the audit's own
  baseline commit, not the corpus-gate commit; the real one is `41bed56`);
  appended a `superseded` block to `FREEZE_STAGE_6_0.md` without rewriting
  its content; replaced the stale "Stage 6.0 заморожено" section in
  `.agents/rules/epistemic_agent.md`; created
  `journal/0009-stage-transition-armed-to-active.yaml` without touching
  `journal/07`. All 5 of this section's own regression checks re-run and
  pass. Only REM-004 through REM-007 and REM-010 through REM-014 remain
  open now.

*Vault copy of this execution log: see `.local-notes/agent-setup-guide.md`
(gitignored — points to the actual Obsidian vault path).*