# Conventions — all the tag systems in one place

Every convention the workspace uses, collected here so you can reference (or change) them
in one spot. The agent learns these from the individual files, but this is the master key.

## 1. Document status tags

First line of every plan / proposal / draft:

```
status: draft | active | on-hold | abandoned | complete
```

| Tag | Meaning | Agent behavior |
|---|---|---|
| `draft` | being written | incomplete — do not rely on |
| `active` | in progress | current truth |
| `on-hold` | paused | reference OK, don't execute |
| `abandoned` | rejected | never carry forward |
| `complete` | done | move to `80_ARCHIVE/` |

## 2. Source tags

Attach to facts so provenance never gets lost.

| Tag | Meaning | Priority |
|---|---|---|
| `[OWNER]` / `[USER]` | you said or confirmed it | highest |
| `[MEM]` | quoted from earlier memory | cite the source |
| `[AI]` / `[INFER]` | the agent inferred it | never the sole basis for a decision |

Conflict resolution: `[OWNER]` > `[MEM]` > `[INFER]`.

## 3. Context classes (the answer gate)

The router (`00_SELF/context_router.md`) classifies each request into one class.
Rename these to fit your life — the letters are just handles.

| Code | Context | Example triggers |
|---|---|---|
| A | Primary role / public work | your main craft, brand, output |
| B | Business / operations | money-in, clients, deals |
| C | Personal taste | "which do you like", aesthetics |
| D | Life events | moving, marriage, big transitions |
| E | Investing / finance | portfolio, buy/sell |
| F | Relationships / emotions | people, conflict, feelings |
| G | Tech / automation | code, scripts, this workspace itself |

## 4. Principle layers (what the gate switches)

| Layer | Name | Reference file |
|---|---|---|
| L1 | Public-persona / brand absolutes | global `CLAUDE.md` |
| L2 | Personal taste filter | `identity/character.md` |
| L3 | Business / ops principles | domain `CLAUDE.md` |
| L4 | Investment thesis + patterns | `decisions/feedback_patterns.md` |
| L5 | Relationship context | `people/people.md` |
| L6 | Tech execution rules | global `CLAUDE.md` |

**The critical rule:** in personal-taste, life-event, investment, and relationship
contexts (C, D, E, F), the public-persona layer **L1 is forced OFF**. Your brand
strategy has no business steering your private life.

## 5. Tier loading

| Tier | When | What |
|---|---|---|
| Tier 1 | auto-injected every session | `shared_memory.md`, `todo.md` |
| Tier 2 | on demand, by request type | decisions, identity, project memory |

## 6. Project-memory frontmatter

Every `memory/projects/{slug}.md` starts with:

```yaml
---
project: {{Project name}}
slug: kebab-case-slug
status: active | on-hold | abandoned | complete
owners: [you, ...]
trigger_keywords: [keyword1, keyword2, ...]
last_updated: YYYY-MM-DD
---
```

`trigger_keywords` is the load switch — the agent opens this file only when the incoming
message matches one of these.

## 7. File naming

| Pattern | Used for |
|---|---|
| `YYYYMMDD_domain_title.md` | dated deliverables / archived docs |
| `{slug}.md` | project memory files |
| `_TEMPLATE.md`, `_PROJECT_TEMPLATE/` | copy-me scaffolds (leading underscore = template) |
| `<name>.example` | tracked seed for a personal-data file; `bootstrap.sh` copies it to the git-ignored live `<name>` |

## 7b. Framework vs your data (the separation that keeps updates safe)

- **Framework** (tracked, updatable): every `CLAUDE.md` router, `context_router.md`, docs,
  skills, tools, `_TEMPLATE`s, `INDEX.md`. Pull upstream to improve these ([UPDATE.md]).
- **Your data** (git-ignored, private): the live files created from `*.example` seeds —
  identity, people, decisions, memory — plus your real `10_WORK/`, `20_DOMAINS/`, `50_LIFE/`,
  `90_SHARED/` content. Never committed; framework updates never touch them.

The rule: **don't put personal content in a tracked framework file.** If a framework file
needs to hold something personal, make an `.example` seed and let bootstrap create the live
copy.

## 8. Change-log numbering

When you change a standing rule, log it as `CHG-1`, `CHG-2`, … in a changelog so the
reasoning survives. Guidelines evolve; the numbers let you trace why.

## 9. The simple-record gate

When a message contains a plain record verb (*note / save / log / add / write down*),
the agent switches to record-only mode:
1. Extract only from the message itself.
2. Don't pull in other memory/context.
3. No inference, no options, no recommendations.
4. Self-check once before writing: "is this a record request or an analysis request?"

This stops the agent from turning "just save this phone number" into a five-paragraph
strategic briefing.

## 10. Context budget (the diet rule)

Instruction files compete with your actual work for the model's attention. Long-context
research ("context rot") shows adherence drops as always-loaded text grows — and rules
buried mid-file get ignored first.

- Every `CLAUDE.md` stays **≤ 200 lines**; aim for 80–120.
- Must-follow rules live in the **top 40 lines** (the model reads top-down).
- Full text (principle documents, code templates, command tables) lives in **one
  canonical file**; routers keep a one-line pointer to it. Never duplicate a rule in two
  files — duplicates drift apart and you won't notice which one the agent obeyed.
- If the agent keeps breaking the same rule, don't write the rule louder — **make it a
  hook** (§9 is one; `tools/hooks/context_gate.py` is another). Enforcement beats prose.
- Memory only grows unless something shrinks it: roll `shared_memory.md` monthly with
  `tools/split_shared_memory.py`.
