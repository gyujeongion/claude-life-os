# Changelog

## v1.0 — 2026-07-15

Initial release.

- Concentric-circle workspace template: `00_SELF` (identity, memory, decisions, people)
  → `10_WORK` → `20_DOMAINS` → `30_KNOWLEDGE` → `40_SYSTEMS` → `50_LIFE` → `80_ARCHIVE`,
  plus an isolated `90_SHARED` companion-agent ring.
- Master router `CLAUDE.md` (navigation gate) + `00_SELF/context_router.md` (answer gate:
  classify the request, switch principle layers — public persona forced OFF in personal
  contexts).
- Agent-run onboarding interview (`ONBOARDING.md`) — "Set this up for me."
- Memory system: five layers with on-demand project loading (`MEMORY_RULES.md`) and a
  monthly rolling tool (`tools/split_shared_memory.py`).
- Enforcement over prose: optional hooks — Tier-1 auto-load (SessionStart) and a
  personal-context gate (`tools/hooks/context_gate.py`, UserPromptSubmit).
- Conventions in one place (`docs/CONVENTIONS.md`): status tags, source tags, context
  classes, tier loading, the simple-record gate, and the context-budget (diet) rule.
- **Framework / data separation** — personal files ship as tracked `*.example` seeds;
  `tools/bootstrap.sh` creates git-ignored live copies. Your data is **private by
  default** (never committed, even in a public fork), and framework updates leave it
  untouched. Update/uninstall paths: `UPDATE.md`, `UNINSTALL.md`.
- **One-prompt install** (`INSTALL.md`): "Read INSTALL.md and set this up for me."
- **Safe hook installer** (`tools/install_hooks.py`) — merges the SessionStart + context
  gate hooks into `~/.claude/settings.json` idempotently, never clobbering existing config.
- **Optional power-ups:**
  - `skills/add` — capture-and-file skill: brain-dump anything, the agent routes each
    piece into the right workspace file (merge, never overwrite).
  - `skills/stt` — Deepgram speech-to-text (bring your own key) that feeds into `add`.
  - `extras/conversation-memory` — a compact, self-hosted semantic memory: index Claude
    Code logs, recall relevant past turns via a local API + injection hook. Includes an
    agent-led build guide. Retrieval gate judges distribution shape (not one threshold);
    injection is framed as fallible.
