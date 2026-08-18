# STAGE 6.1 ACTIVATION

Цей документ фіксує перехід Stage 6.0 зі стану `FROZEN` у `ACTIVE` після
виконання тригера, зафіксованого в `FREEZE_STAGE_6_0.md`. Виконано за
планом `docs/REMEDIATION_PLAN_v1.md` (REM-001, ECA-001).

```yaml
trigger: "externally attributable, independently retrievable historical corpus"
evidence: journal/0008-gretil-corpus-gate.yaml
trigger_commit: "41bed56dbaf85f71baefbd7663b07a7bc95d6819"  # feat: gate REAL GRETIL Kasika corpus into blind pipeline (L-002 RESOLVED)
trigger_date: "2026-08-15"
activated: "2026-08-18"

unlocked:
  - "L-001 testing (blind semantic reconstruction) on the REAL GRETIL corpus"

still_forbidden:
  - "Treating synthetic datasets (ksetra/astadhyayi/blind/semantic_batch_2/, external_data/kasika_corpus.json) as historical evidence"
  - "Claims of linguistic independence of the 42 classes until L-001 completes"

supersedes:
  - document: FREEZE_STAGE_6_0.md
    scope: "state only -- the freeze document itself is not deleted or rewritten, see its own superseded block"
```

## Провенанс цього переходу

- `journal/07_epistemic_rearming.md` (2026-08-15) зафіксував стан **до**
  здобуття корпусу: `FROZEN -> ARMED / WAITING_FOR_CORPUS`.
- `journal/0008-gretil-corpus-gate.yaml` (commit `41bed56`, 2026-08-15)
  зафіксував **здобуття** корпусу — GRETIL Kāśikāvṛtti (Sharma ed.) +
  Aṣṭādhyāyī (Baums), sha256 manifest, 3951 sūtras parsed.
- Між цими двома фактами не існувало формального документа переходу —
  саме цю прогалину усуває `journal/0009-stage-transition-armed-to-active.yaml`
  і цей документ.

## Що це НЕ означає

- Це не підтверджує лінгвістичну незалежність канонічних 42 класів від
  Śiva-sūtras (L-001 залишається `OPEN`, лише тепер тестується на
  справжньому корпусі замість заблокованого стану).
- Це не скасовує заборону на синтетичні дані як historical evidence.
- Це не робить `FREEZE_STAGE_6_0.md` недійсним документом — він лишається
  точним записом стану на момент написання, лише позначений `superseded`
  щодо поточного стану проєкту.
