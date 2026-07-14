# CLAUDE.md — Life Agent Workspace (master router)

> This is the **master entry point** for your personal AI workspace.
> Claude Code reads this file first, then routes to the right folder.
> Fill in the `{{PLACEHOLDER}}` tokens once, then let the structure work.
>
> 이 파일은 개인 AI 워크스페이스의 **마스터 진입점**입니다. 클로드 코드가 가장 먼저 읽고,
> 여기서 알맞은 폴더로 라우팅합니다. `{{PLACEHOLDER}}`만 한 번 채우면 됩니다.

**Owner**: {{OWNER_NAME}} | **Language**: {{PRIMARY_LANGUAGE}} | **Timezone**: {{TIMEZONE}}

---

> ⚙️ **FIRST-RUN TRIGGER (agent, read this first).** If any `{{PLACEHOLDER}}` token still
> appears above or anywhere in this workspace — or the user asks you to "set this up" —
> **stop and run `ONBOARDING.md` now**, before answering anything else. It's an interview
> script that tailors this generic template to the user's actual life and domains. Do not
> just fill in a name; follow the whole script so the workspace becomes genuinely theirs.
>
> ⚙️ **최초 실행 트리거.** 위쪽이나 워크스페이스 어디든 `{{PLACEHOLDER}}`가 남아있거나
> 사용자가 "세팅해줘"라고 하면 — 다른 답변보다 **먼저 `ONBOARDING.md`를 실행**하세요.
> 이름만 채우지 말고 스크립트 전체를 따라 사용자 삶·도메인에 맞게 재구성하세요.

---

## The idea in one paragraph

This workspace is your **life, organized as concentric circles** so an AI agent can
navigate it the way you would. The center (`00_SELF`) is who you are. The rings move
outward: active work, ongoing roles, knowledge, systems, personal life. Every folder
has its own `CLAUDE.md` that tells the agent what lives there and when to open it. The
agent never scans everything — it follows pointers, exactly like a human opening the
one drawer they need.

---

## Session start — file loading strategy

### Tier 1 — always loaded (auto-injected every session)
```
1. 00_SELF/memory/shared_memory.md   ← recent cross-session context
2. 00_SELF/memory/todo.md            ← only mention items due today/tomorrow
```
> Wire these into a SessionStart hook so they load automatically. See docs/SETUP.md.
> **Drift guard:** if the hook is not actually wired (or you can't verify it), Read these
> two files yourself at session start. A doc that *claims* auto-injection while nothing is
> wired is the most common way this tier silently dies.

### Tier 2 — on demand (loaded only when the request type calls for it)
```
3. 00_SELF/decisions/decisions_log.md       ← strategy / planning requests
4. 00_SELF/identity/character.md            ← taste / preference judgments
5. 00_SELF/memory/projects/INDEX.md         ← when a project keyword is detected
   → match trigger_keywords, then load only that projects/{slug}.md
   → rules: 00_SELF/memory/MEMORY_RULES.md
```

---

## Navigation protocol

```
request arrives
  → pass the 00_SELF/context_router.md gate (classify context, decide which principles apply)
  → use the mapping table below to pick the folder
  → read that folder's CLAUDE.md
  → open ONLY the specific files you need
```

**Never**: list the whole root, wander into unrelated folders, print secrets, open
files "just for reference."

---

## Request → folder mapping

| Request type | Folder | Entry file |
|---|---|---|
| Who you are · identity · taste · memory | `00_SELF/` | `00_SELF/CLAUDE.md` |
| People · relationships | `00_SELF/people/` | `people.md` |
| Confirmed decisions · rejection history | `00_SELF/decisions/` | `decisions_log.md` |
| Active projects (have a deadline) | `10_WORK/` | `10_WORK/CLAUDE.md` |
| Ongoing roles / domains (no deadline) | `20_DOMAINS/` | `20_DOMAINS/CLAUDE.md` |
| Research · analysis · knowledge | `30_KNOWLEDGE/` | `30_KNOWLEDGE/CLAUDE.md` |
| Code · automation · infrastructure | `40_SYSTEMS/` | `40_SYSTEMS/CLAUDE.md` |
| Money · family · health · personal life | `50_LIFE/` | `50_LIFE/CLAUDE.md` |
| Done · inactive | `80_ARCHIVE/` | — |
| Shared / companion agent (isolated) | `90_SHARED/` | `90_SHARED/CLAUDE.md` |
| A note/memo/record request | → identify the domain above, save into that doc | that domain's folder |
| Unclear | — | ask the owner directly |

---

## Document status tags

Every plan/proposal/draft starts its first line with one of these:

```
status: draft | active | on-hold | abandoned | complete
```

| Tag | Meaning | How the agent treats it |
|---|---|---|
| `draft` | being written | incomplete — do not rely on |
| `active` | in progress | use as current truth |
| `on-hold` | paused | reference OK, do not execute |
| `abandoned` | rejected | never carry into future plans (reason → `feedback_patterns.md`) |
| `complete` | done | candidate to move into `80_ARCHIVE/` |

---

## Source separation

| Tag | Meaning | Where it lives |
|---|---|---|
| `[OWNER]` | the owner said/confirmed it | `00_SELF/decisions/` |
| `[AI]` | the agent inferred/proposed it | `30_KNOWLEDGE/` |

On conflict, `[OWNER]` always wins.

---

## Rejection-capture protocol

When the owner rejects a proposal and gives a reason:

1. Mark that document `status: abandoned`.
2. Classify the reason:
   - taste / disposition → `00_SELF/decisions/feedback_patterns.md`
   - direction / brand → the relevant identity file
   - a changed decision → `00_SELF/decisions/decisions_log.md`
3. The next time you plan, that pattern is filtered automatically.

---

## AI self-observation (optional but powerful)

The agent may, on its own, log **repeated** behavioral patterns it notices in the
owner to `00_SELF/identity/character_ai_mirror.md`. Rules:
- only patterns seen **2+ times** (never one-offs)
- descriptive, not evaluative ("tends to…", never "is bad at…")
- after logging, tell the owner in one line

---

## When you plan or strategize (checklist)

1. `00_SELF/memory/SYNC_AXIS.md` — does this align with the owner's core axis?
2. `00_SELF/decisions/decisions_log.md` — any conflict with a confirmed decision?
3. `00_SELF/decisions/feedback_patterns.md` — apply past rejection filters.
4. `00_SELF/identity/character.md` — does this fit the owner's disposition?
5. Keep analysis docs and proposal docs **separate**.
6. When revising, preserve the old version (`_v1`, `_v2`).

---

## The two gates (this is the whole trick)

1. **Navigation gate** (this file): decides *which files to open*.
2. **Answer gate** (`00_SELF/context_router.md`): decides *which principles to apply*
   to the answer — because advice about your career should not be governed by the same
   rules as advice about your health or your relationships.

Read `docs/ARCHITECTURE.md` for why it's built this way.
