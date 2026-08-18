# How to work with Sarvam (for any repo's agent)

Status: **OPERATIONAL GUIDE**, based on direct testing in `shiva-sutras`,
2026-08-18. Not a claim about Sanskrit, not architectural advice — just
"here's how to not waste your context on this tool."

*Vault copy with a doc-per-finding breakdown: see `.local-notes/agent-setup-guide.md`
(gitignored — that file has the actual vault path; kept out of git deliberately).*

## What it is, what it isn't

- Sarvam (`sarvam-105b`) is an **independent linguistic hypothesis generator**,
  not a source of truth. Use it for Indic terminology, transliteration,
  translation, alternative readings. Verify anything substantive against
  primary sources before recording it as a fact.
- It's reachable two ways — pick based on where you're calling from:
  - **MCP tools** (`mcp__sarvam-ai__sarvam_tools_*`) — if you're a Claude Code
    session with the `sarvam-ai` MCP server configured (see
    `claude_desktop_config.json`, `mcpServers.sarvam-ai`). Use this by default.
  - **HTTP proxy** (`C:/GitHub/sarvam-proxy/server.py`, OpenAI-compatible,
    `POST /v1/chat/completions`) — if you're a plain script/pipeline outside
    Claude Code that needs a normal HTTP endpoint.
- Don't write a third wrapper. Both already exist and cover every case we've
  hit so far.

## The one bug you need to know about

`sarvam-105b` is a **reasoning model**. It thinks before it answers, and those
reasoning tokens are billed against the same `max_tokens` budget as the visible
answer (`reasoning_content` vs `content`, but both come out of one pool).

Symptom: you set `max_tokens` (anything from 50 to 4096 — 4096 is the hard
ceiling on the starter tier), the call "succeeds" with `finish_reason: "length"`,
but `content` is an **empty string**. The whole budget got eaten by invisible
reasoning; nothing was left to write the actual answer.

We tried the documented fix (`reasoning_effort: null` to disable thinking mode
— see `docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview`).
It is **not** in the MCP tool's declared parameter schema (only `messages`,
`model`, `max_tokens`, `stream`, `temperature`, `top_p` are declared), and
passing it anyway worked once and then failed on an identical retry — treat it
as unreliable, not a fix.

### What actually works

1. **Don't set `max_tokens` at all** for anything short — a single fact, a
   transliteration, a yes/no with one line of justification. Confirmed working
   twice in a row (IAST diacritic question, Devanagari→IAST transliteration),
   both `finish_reason: "stop"`, real content.
2. **For anything bigger, split it into several small calls instead of one big
   one.** A single call asking for "4 axes of comparison, explained" reliably
   died empty even at the 4096 ceiling. Asking for one fact at a time works.
3. If you must cap length, ask the model *in the prompt* to be terse ("one
   sentence", "bullet list, max 3 items, under 15 words each") rather than
   relying on `max_tokens` to cut it off — a truncated answer is at least a
   real (if incomplete) answer; a token-limited one is often nothing at all.

## Using it correctly (per the epistemic-coordination principle)

Don't ask Sarvam to confirm a conclusion you already reached — that's not
independent verification, that's asking it to agree with you. Ask the same
*primary* question you asked yourself, cold, with no hint of your own answer,
then compare afterward. If every agent agrees immediately, check whether they
were actually asked independently.

Good prompt shape:
```
system: "You are an independent linguistic reviewer. Answer briefly and
directly. No prior context about any project."
user: <the raw question or raw data, nothing about your hypothesis>
```

Log the result with its actual epistemic status (`HYPOTHESIS`, not `FACT`),
Sarvam's exact output, and whether/how it was reconciled with your own
independent analysis — see `hypotheses/independent-claims-h001-h003-sarvam.yaml`
in `shiva-sutras` for the format this repo uses.

## Quick reference

| Need | Tool |
|---|---|
| Chat/reasoning-model completion | `mcp__sarvam-ai__sarvam_tools_llm_complete` |
| Translation | `mcp__sarvam-ai__sarvam_tools_translate` |
| Transliteration (script conversion) | `mcp__sarvam-ai__sarvam_tools_transliterate` |
| Language/script identification | `mcp__sarvam-ai__sarvam_tools_identify_language` |
| STT / TTS | `sarvam_tools_stt_*` / `sarvam_tools_tts_*` |
| From a non-Claude script | `POST http://<sarvam-proxy host>/v1/chat/completions` |

Full source: `C:/GitHub/shiva-sutras/docs/cross-repo-ecosystem-findings-2026-08-18.md`
(Finding 3) has the raw evidence — request/response pairs, timings, exact
failure mode — if you want to double-check any of this before trusting it.

---

## Full capability inventory (from official docs + third-party sources, 2026-08-18)

Status: **compiled from public sources**, not independently verified end-to-end
by this repo the way Finding 3 was (that one *was* independently reproduced —
see above). Treat model-benchmark numbers and reviewer opinions as
secondhand claims, not this repo's own evidence. Sources listed per section.

### The 14 MCP tools, in full

Runtime tools (`sarvam_tools_*`, calls the live API):

| Tool | Does |
|---|---|
| `sarvam_llm_complete` | Chat completion, `sarvam-105b` (or `-30b`) — see reasoning-token caveat above |
| `sarvam_translate` | Document-level translation across 22 official Indian languages, long-context, not just sentence-by-sentence |
| `sarvam_transliterate` | Script conversion (e.g. romanized ↔ native script) |
| `sarvam_identify_language` | Detects language + script from text |
| `sarvam_text_analytics` | Typed Q&A extraction over a text blob |
| `sarvam_stt_transcribe` | Audio → text. Five output modes: transcribe, translate, verbatim, transliterate, codemix |
| `sarvam_stt_batch_submit` / `_batch_status` | Async batch STT for longer audio |
| `sarvam_tts_speak` / `_tts_stream` | Text → speech (Bulbul model), 10-11 Indian languages, streamed or file output |
| `sarvam_vision_extract` / `_vision_job_status` | Document intelligence: OCR, table-to-HTML, structured extraction from images/PDFs |
| `sarvam_pronunciation_list` / `_get` / `_create` / `_delete` | Manage custom pronunciation dictionaries (affects TTS output for specific words) |

Builder tools (`sarvam_code_*`, no API call, just dev-assist): `sarvam_code_recommend_model`,
`sarvam_code_api_reference`, `sarvam_code_languages`, `sarvam_code_pricing`,
`sarvam_code_snippet`, `sarvam_code_speakers`, `sarvam_code_validate_request`.
Use these to figure out *which* runtime tool/model fits a task before calling it —
free, no API key needed, no budget consumed.

*Source: [github.com/sarvamai/sarvam-mcp](https://github.com/sarvamai/sarvam-mcp),
[docs.sarvam.ai/api/developer-tools/mcp](https://docs.sarvam.ai/api/developer-tools/mcp)*

### Model characteristics (sarvam-105b)

- Mixture-of-Experts, 10.3B active parameters (of a larger total) — cheaper to
  run per-call than a dense model of similar quality.
- 128K context window.
- Reasoning-model training: reward-shaped for structured reasoning, tool use,
  and concise final answers — but see Finding 3 above, the "concise" part
  doesn't reliably survive a tight `max_tokens`.
- Benchmarked (per Sarvam's own release) as competitive with frontier
  closed-source models on agentic/tool-use tasks (49.5 BrowseComp, 68.3 Tau2)
  and reasoning/math/code — these are **vendor-reported numbers**, not
  something this repo re-ran.
- 23 Indic languages supported natively, including romanized and code-mixed
  (Hinglish-style) input styles.

*Source: [sarvam.ai/blogs/sarvam-30b-105b](https://www.sarvam.ai/blogs/sarvam-30b-105b),
[explainx.ai Sarvam AI capabilities guide](https://explainx.ai/blog/sarvam-ai-capabilities-api-models-guide-2026)*

### Independent/third-party review findings (not vendor-reported)

From an independent review site, useful as a sanity check on vendor claims:

- **Vision/OCR accuracy**: ~75% on image understanding; may miss words/lines
  in complex images. Don't treat `sarvam_vision_extract` output as
  ground-truth without spot-checking on anything that matters.
- **File limits**: images capped at 5MB; documents capped at 5 pages without
  direct API access (vs. the MCP/dashboard front-end).
- **Chart-to-markdown**: produces full tables rather than concise summaries —
  expect verbose output, plan token budget accordingly.
- **Best fit**: Indic-language and voice-driven workflows specifically; for
  English-only work, reviewer notes other tools may be more refined — matches
  this repo's own stance that Sarvam is a *specialist*, not a general
  replacement for other tools.

*Source: [alloypress.com/reviews/sarvam-ai-review](https://alloypress.com/reviews/sarvam-ai-review)*

### What we could NOT find on forums/GitHub

Searched GitHub issues/discussions (`ggml-org/llama.cpp`, `ollama/ollama`,
`huggingface.co/sarvamai/sarvam-105b` discussions) and general web search for
prior reports of the reasoning-token/`max_tokens` truncation behavior
documented in Finding 3 above. **Found nothing** — no forum post, GitHub
issue, or review mentions it. Two possible readings, both worth keeping in
mind: (a) this is a real, under-reported gap in Sarvam's docs/MCP tool that
we're among the first to hit and write down, or (b) it's specific to this
particular MCP tool version/starter-tier interaction and hasn't affected
other integration paths (direct API, other SDKs) the same way. Don't treat
Finding 3 as "everyone knows this" — it isn't documented anywhere else we
could find.

*Sources checked: [github.com/ggml-org/llama.cpp/issues/20175](https://github.com/ggml-org/llama.cpp/issues/20175),
[github.com/ollama/ollama/issues/16242](https://github.com/ollama/ollama/issues/16242),
[huggingface.co/sarvamai/sarvam-105b/discussions](https://huggingface.co/sarvamai/sarvam-105b/discussions)*
