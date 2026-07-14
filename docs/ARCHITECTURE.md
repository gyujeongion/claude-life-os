# Architecture — why concentric circles

This document explains the *why* behind the folder layout. If you just want to get
started, read [SETUP.md](SETUP.md) instead.

## The problem this solves

A personal AI agent fails in two opposite ways:

1. **It knows nothing** — every session starts from zero, you re-explain your life daily.
2. **It knows everything at once** — you dump your whole life into one context window,
   the agent drowns, and it applies your work persona to your marriage.

The fix is not "more memory." It's **structured retrieval + context-scoped principles.**

## Concentric circles

Your life is not a flat list of folders. It has a center — *you* — and everything
else radiates outward with decreasing intimacy:

```
00_SELF     the self          most intimate, always relevant
10_WORK     what you're doing  time-boxed, has deadlines
20_DOMAINS  who you are to others   ongoing roles, no deadline
30_KNOWLEDGE what you know     reference material
40_SYSTEMS  what you've built  tools and automation
50_LIFE     the logistics of living   money, family, health
80_ARCHIVE  the past           done, kept for reference
90_SHARED   a separate self    an isolated agent for shared contexts
```

The numbering is deliberate. `00` is the core; higher numbers are further out. An
agent answering a question starts at the center and walks outward **only as far as
the question requires.** A question about "what should I cook tonight" never needs to
touch `20_DOMAINS`. A question about your five-year direction starts at `00_SELF` and
may pull from everything.

### Why 10-step gaps (00, 10, 20…)?

So you can insert new rings without renumbering. Want a `15_LEARNING` ring between work
and domains? It slots in. The gaps are on purpose.

## The two gates

This is the part worth stealing even if you throw away everything else.

### Gate 1 — Navigation (the `CLAUDE.md` chain)

Every folder has a `CLAUDE.md` that is a **signpost, not a container**. It says:
"here's what lives in this folder, and here's the one file you want for *this* request."

```
~/.claude/CLAUDE.md          global rules (all projects)
  └─ CLAUDE.md               workspace master router (request → folder table)
       └─ 00_SELF/CLAUDE.md  self hub index
       └─ 10_WORK/CLAUDE.md  project index
       └─ 20_DOMAINS/CLAUDE.md → {DOMAIN}/CLAUDE.md   domain-specific rules
       └─ …
```

The agent never `ls`-es your whole life. It reads one signpost, follows one pointer,
opens one file. This keeps the context window small and the answers sharp.

### Gate 2 — Answer (`00_SELF/context_router.md`)

Navigation decides *what the agent reads*. The answer gate decides *who the agent is*
when it responds.

Consider: the same person asks the same agent —
- "Should I take this job?" → career-context rules apply
- "Should I text my ex back?" → relationship-context rules apply, career rules **must not**
- "Should I sell this stock?" → investment-context rules apply

If one global rulebook governed all three, the agent would give you brand-consistent,
strategically-optimized advice about your *love life* — which is exactly wrong.

The router classifies each request into a **context** (A–G), then switches
**principle-layers** (L1–L6) on or off. A brand/public-persona layer that's essential
for work gets **forced off** for personal, relational, and health contexts. See
[CONVENTIONS.md](CONVENTIONS.md) for the full layer table.

## Memory: three depths, loaded on demand

```
Global memory   agent_brain/MEMORY.md   auto-loaded every session   (facts, environment)
Project memory  memory/projects/{slug}.md  loaded ONLY when a trigger_keyword matches
Session log     memory/shared_memory.md    cross-session handoff, recent months only
```

The registry (`memory/projects/INDEX.md`) maps trigger keywords → project files. The
agent matches the incoming message against keywords and loads *only* the matching
project. No keyword match → it answers from global memory alone. This is how you can
have 50 projects on file without ever blowing the context window.

## The feedback loop

The system gets smarter by remembering what you *reject*, not just what you accept:

```
you reject a proposal + give a reason
  → doc marked status: abandoned
  → reason filed in feedback_patterns.md
  → next time the agent plans, that pattern is filtered out automatically
```

Say "no, I hate that" once. You won't see it again.

## Source-of-truth discipline

Every fact carries a tag: `[OWNER]` (you said it) or `[AI]` (the agent guessed it).
When they conflict, owner wins — always, no exceptions. This prevents the slow drift
where an agent's confident guesses harden into "facts" about your life.

## Adapt it

Nothing here is sacred except the two gates and the center-out principle. Rename rings,
delete `90_SHARED` if you don't need a second agent, add rings for what matters to you.
The architecture is a starting shape, not a cage.
