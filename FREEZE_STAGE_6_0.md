# FREEZE MANIFEST: STAGE 6.0

Цей документ фіксує замороження Етапу 6.0 (Blind Semantic Reconstruction Infrastructure & Epistemic Pipeline). Архітектура проєкту визнана методологічно зрілою, але подальше масштабування призупинено до виконання тригера.

```yaml
freeze_date: "2026-08-15"
frozen_commit: "TBD"  # Will be set at next commit
semantic_schema_version: "2.1"
validator_version: "v2"
candidate_harvest_version: "v5.1"

known_open_problems:
  - "Linguistic Independence Theorem: The independence of the 42 classes from the Śiva-sūtras cannot be proven until an independent historical corpus is fully reconstructed."

known_invalid_synthetic_datasets:
  - "ksetra/astadhyayi/blind/semantic_batch_2/ (30-sutra corpus)"
  - "external_data/kasika_corpus.json (Repository-local generated data)"

next_allowed_trigger:
  - "Stage 6 resumes only when an externally attributable, independently retrievable historical corpus is available."
```

Будь-які спроби "згенерувати" додаткові сутри або продовжити роботу пайплайну на синтетичних даних заборонені. Система очікує підключення зовнішнього достовірного джерела.
