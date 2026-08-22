# shiva-sutras — agent notes

Śiva-sūtra canon / Ksetra corpus provenance authority. Do not edit source texts; see NOTICE.md for corpus usage terms.

## Agent Guard (M0 — PROPOSED, 2026-08-22)

План executable-constitution guardrails для агентських сесій:
`/home/agents/ecosystem/plans/AGENT-GUARD-M0.md`
Машинні гачки на C1/C7/C9/C11 (ox-alpha constitution v1.2).
Статус: план. Прочитайте перед write-heavy роботою.

## NLP / Embeddings tooling (2026-08-22)

Для NLP-задач (ембедінги, семантична класифікація, BGE-M3): системний
python3 НЕ має torch. Використовуй
`/home/agents/GitHub/FlagEmbedding/.venv/bin/python`.
Конфіг і готові індекси: `/home/agents/GitHub/vault-semantic-mcp/`
(корпусні ембедінги вже в `data/sanskrit_embeddings.jsonl` — перевикористовуй).
GPU лише 4GB — батчі ≤4, fp16, не перераховувати зайве.
Повний рецепт: `/home/agents/ecosystem/memory/nlp-tooling-setup.md`.
