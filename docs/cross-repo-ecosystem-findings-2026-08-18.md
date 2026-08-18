# Cross-Repo Ecosystem Findings — 2026-08-18

Status: **FINDINGS + PROPOSALS**, not architectural advice, not implemented.

Scope: observations about `my-lisp` / `fpga-lisp` / `cml` / `tauricode` / `my-idea`,
made from `shiva-sutras` while auditing sibling repos on disk (`C:/GitHub/*`).
Per [`docs/epistemic-coordination.md`](epistemic-coordination.md) §3, this repo does
not issue architectural advice to downstream/lateral projects — these are `finding`
and `proposal` artifacts for the owning repos to accept, reject, or ignore. No sibling
file was edited to produce this document.

*Vault copy, split one-note-per-finding: see `.local-notes/agent-setup-guide.md`
(gitignored — points to the actual Obsidian vault path, kept out of git).*

---

## Finding 1 — Language-contract version drift (CONFIRMED, then RESOLVED by sibling agents)

> **UPDATE 2026-08-18 (later same day):** Re-verified during a scope-check pass
> (`SHIVA-PERIODIC-DRIFT-REVERIFY`). Both repos already fixed this independently:
> `fpga-lisp/AGENTS.md` commit `6bc53d6` ("Fix stale language-contract version
> claim in AGENTS.md (1.0 -> 2.0)", 2026-08-18 04:42:43+03:00) and
> `cml/AGENTS.md` commit `146fc1d` ("Fix stale contract-version claims in
> AGENTS.md/compatibility.my (1.0 -> 2.0)", 2026-08-18 04:50:49+03:00) — both
> landed *before or during* the drafting of this document. The original
> finding below is left as-written for the audit trail; treat it as
> **historical**, not current state. Neither repo now hardcodes a bare "1.0" —
> both point at `language-contract.my`'s own `(major . minor)` cons cell as
> source of truth, exactly as this document's proposed fix suggested.

- **Authoritative source**: `my-lisp/language-contract.my:72` — `((major . 2) (minor . 0) ...)`
  (commit `d287a16` last touched this file, 2026-08-15).
- **Stale references**:
  - `fpga-lisp/AGENTS.md:49` — "Language contract version 1.0 (`language-contract.my`)."
    (file as of commit `6bc53d6`, 2026-08-18)
  - `cml/AGENTS.md:11` — "Language contract version 1.0 (`language-contract.my`)."
    (file as of commit `c82027d`, 2026-08-18)
- **Impact**: an agent trusting either AGENTS.md prose would believe the live contract
  is 1.0 when it is actually 2.0 (a *major* bump — semantics changed, not just additive).
- **Proposed fix** (for fpga-lisp/cml owners, not applied here): replace the hardcoded
  "version 1.0" string with a pointer to `language-contract.my`'s own `(major . minor)`
  cons cell as the single source of truth, so prose can't drift again. A one-line
  wording change, not a structural one.

## Finding 2 — cml has no swarm-node coordination note (CONFIRMED GAP, then RESOLVED)

> **UPDATE 2026-08-18 (later same day):** `cml/AGENTS.md` commit `c82027d`
> ("Fix stale AGENTS.md: add swarm-node session-start, refresh
> coordination/backend info", 2026-08-18 05:05:43+03:00) added the swarm-node
> section (`cml/AGENTS.md:11-22`, port 9105, connects to `127.0.0.1:9101`).
> cml now documents the same P2P model as my-lisp/fpga-lisp. Historical below.

- `my-lisp/AGENTS.md:5-16` documents a 2026-08-12 migration off `:9999` onto
  `swarm-node` (P2P), with an explicit "prose is not authoritative, read this note"
  caveat.
- `fpga-lisp/AGENTS.md:9-24` documents the same migration and gives connection
  parameters (`--port 9103 --connect 127.0.0.1:9101`).
- `cml/AGENTS.md:100-109` ("Cross-session coordination protocol") describes a
  *third*, independent scheme: durable facts in `ecosystem-status.md`/`.my`,
  synchronous asks via direct messages — no mention of swarm-node, `:9101`, or
  `:9999` in that section.
- This is not necessarily wrong (per this project's own rule 5: "divergence is a
  result, not automatically a bug to fix") — but it is currently **undocumented**
  whether cml deliberately stays off swarm-node or simply hasn't been updated.
- **Proposed next step** (for cml owner): add one line to `cml/AGENTS.md` stating
  explicitly whether cml participates in swarm-node or intentionally uses the
  status-file model only, and why.

## Finding 3 — sarvam-proxy / sarvam-mcp reasoning-token truncation bug (CONFIRMED, reproduced)

Not part of the original recommendation list, but discovered while testing the
MCP-based Sarvam integration (`mcp__sarvam-ai__sarvam_tools_llm_complete`):

- `sarvam-105b` is a reasoning model. Reasoning tokens are billed against
  `max_tokens` and returned separately as `reasoning_content`.
- With `max_tokens` explicitly set (any value from 50 to 4096, the starter-tier
  ceiling), non-trivial prompts frequently return `content: ""`,
  `finish_reason: "length"` — the entire budget is consumed by invisible
  reasoning, nothing is left for the visible answer.
- Sarvam's own docs (`docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview`)
  say to pass `reasoning_effort: null` to disable thinking mode. The MCP tool
  schema for `sarvam_tools_llm_complete` does **not** declare a `reasoning_effort`
  parameter (only `messages`, `model`, `max_tokens`, `stream`, `temperature`,
  `top_p`) — passing it anyway worked intermittently (succeeded once, failed on
  retries with an identical shape of request), consistent with the MCP layer
  silently dropping undeclared fields rather than the API itself being flaky.
- **Practical mitigation** (works reliably): omit `max_tokens` entirely for
  short/simple prompts (model then self-allocates and reasoning finishes before
  running out); for longer prompts, request very short, single-fact answers
  rather than multi-part analyses, and expect to make several small calls
  instead of one large one.
- **Proposed fix** (for whoever owns the `sarvam-mcp` packaging, likely upstream,
  not this ecosystem): expose `reasoning_effort` in the tool's declared schema.

---

## Proposal — Cross-repo drift checker (NOT built, placement undecided)

Sketch only. A script that, for every sibling repo, extracts:

```
claimed contract version   (grep AGENTS.md)
claimed ISA version        (grep AGENTS.md)
claimed coordination port  (grep AGENTS.md)
```

and diffs each against the authoritative machine-readable file
(`language-contract.my`, `isa-contract.my`) in the repo that actually owns it.//
Natural owners per the existing role table: **tauricode** (agent tooling/workspace)
or **my-idea** (observer/status layer) — not `shiva-sutras`, which has no standing
authority over `my-lisp`/`fpga-lisp`/`cml` contracts. Needs an explicit go-ahead
from whichever of those two repos' owners before any code is written there.

## Proposal — Golden Vertical Experiment (NOT built, decision belongs to my-lisp/cml/fpga-lisp)

One expression, same observable result, through the full stack:

```
my-lisp (Rust) == my-lisp (Racket)
        |
        v
       cml
        |
        v
    fpga-lisp
        |
        v
     iverilog
```

Suggested minimal content to exercise real semantic surface: an exact rational,
a lexical closure, a macro defined in `lib/core.my`, and a list structure — not a
reasoning engine, not a large program. This is a proposal for the owners of
`my-lisp`/`cml`/`fpga-lisp` to accept, scope, and run; `shiva-sutras` has no
standing to define or execute it.

---

## Scope-check — SHIVA-SWARM-CONTRACT-01 (adopt Swarm Contract v0.1)

- **Spec located**: `my-lisp/docs/swarm-mesh-v2.md`. Not a draft — M0.1
  through M0.13 are all marked done, with integration tests
  (`crates/swarm-node/tests/integration.rs`) and live cross-machine
  verification (M0.11, a real Tailscale-connected second host). This is
  production coordination infra, not a proposal.
- **`repo.my` format** — confirmed by example, `my-lisp-panini/repo.my`:
  ```lisp
  (repository
    (id my-lisp-panini)
    (role knowledge-compiler)
    (exports panini-claims derivations)
    (imports shiva-claims)
    (capabilities sanskrit symbolic-reasoning documentation)
    (authorities paninian-ontology)
    (non-authorities shiva-canon my-lisp-runtime fpga-hardware))
  ```
  A `shiva-sutras/repo.my` in the same shape (role e.g. `research-lab`,
  `authorities (shiva-canon markers pratyahara-mechanics)`,
  `non-authorities (paninian-ontology my-lisp-runtime fpga-hardware)`)
  is straightforwardly compatible with `docs/epistemic-coordination.md`'s
  upstream-authority stance — the file format itself is just a declaration
  of scope, it doesn't force accepting downstream premises. **Writing this
  file is low-risk and can be done without further check-in.**
- **Actually joining the mesh is a separate, bigger step**: it means
  building `swarm-node` (`cargo build -p swarm-node` from a `my-lisp`
  checkout) and running it as a **persistent background process** that
  opens a TCP listener and dials `127.0.0.1:9101` (my-lisp-1's bootstrap
  node). That's a standing network service, not a one-time file write —
  it should not be started without an explicit go-ahead, per the
  hard-to-reverse/shared-state action guidance this session already
  operates under.
- **Recommendation**: split `SHIVA-SWARM-CONTRACT-01` into two:
  (a) write `repo.my` + `ecosystem/` scaffold now — safe, low-risk;
  (b) actually building and launching `swarm-node` for shiva-sutras —
  needs explicit confirmation, since it's a running network process.

## Provenance

- Surveyed repos: `my-lisp`, `fpga-lisp`, `cml`, `my-idea`, `my-lisp-panini`,
  `tauricode` (all present under `C:/GitHub/`).
- Method: direct file read + `git log -1 --format=%H -- <file>` per repo, no
  agent/prose claims taken at face value.
- Author: `shiva-sutras` Claude Code session, 2026-08-18.
- This document itself is a `finding`/`proposal` artifact, not a `claim` in the
  sense of `docs/claims-export.yaml` (those are Sanskrit/Śiva-sūtra research
  claims; this is ecosystem meta-observation) — kept separate deliberately.
