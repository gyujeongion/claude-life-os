# MEMORY_RULES.md — how memory works

> Defines what goes in which memory layer, how it loads, and how it updates. This is the
> rulebook the agent follows so memory stays useful instead of becoming a junk drawer.
>
> 어떤 정보를 어느 메모리 계층에 넣고, 어떻게 로드하고 갱신하는지 정의합니다.

## 1. The five layers

| Layer | Location | Loading | Holds |
|---|---|---|---|
| Global | `agent_brain/MEMORY.md` | auto, every session | environment facts, core owner profile |
| User | `agent_brain/USER.md` | auto, every session | communication style, delegation prefs |
| Project | `projects/{slug}.md` | on demand (trigger match) | per-project facts + decisions |
| Registry | `projects/INDEX.md` | when a project keyword appears | project list + trigger mapping |
| Session log | `shared_memory.md` | on demand | cross-session handoff, recent months |

## 2. Global memory — what goes in

**Put in:** stable facts (environment, tools, paths, the owner's core profile), things
true across many sessions.
**Never put in:** secrets/keys, fast-changing state, one-off details, anything that
belongs to a single project.
**Size guard:** keep it lean. If it's growing past a screen or two, something belongs in
project memory instead.

## 3. Project memory — structure

Path: `projects/{slug}.md`. Required frontmatter:

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

Standard sections:
1. **Summary** (≤3 lines)
2. **Facts** — each tagged `[USER]` / `[MEM]` / `[INFER]`
3. **Decisions** (with dates)
4. **Open questions**
5. **Next steps** (with owner + due date)
6. **Links**

Source tags: `[USER]` (owner said it) > `[MEM]` (from earlier memory) > `[INFER]` (agent
guessed — never the sole basis for a decision).

## 4. Trigger → loading

```
message arrives
  → try to match projects/INDEX.md trigger_keywords
  → load ONLY the matched projects/{slug}.md
  → no auto-reading of unrelated project files
  → no match → answer from global memory alone
```

This is what lets you keep dozens of projects on file without ever overloading context.

## 5. Simple-record mode

If the message is a plain record request (*note / save / add / log*), extract from the
message only. Don't pull in other memory. Don't infer or recommend. (Full rule in
`../context_router.md` Phase 0.)

## 6. Update protocol

| Event | Action |
|---|---|
| New project | create `{slug}.md` + add a row to `INDEX.md` |
| Update | edit the `{slug}.md`, bump `last_updated` |
| Complete | set `status: complete`, move toward `80_ARCHIVE/` |
| Rejected | set `status: abandoned`, file the reason in `../decisions/feedback_patterns.md` |

## 7. Search & indexing

The registry (`projects/INDEX.md`) is the index. Keep its `trigger_keywords` honest and
specific — vague keywords cause the wrong project to load. That's the only "search" the
system needs at small scale; add a vector/RAG layer later only if you outgrow it.
