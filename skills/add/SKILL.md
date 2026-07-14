---
name: add
description: |
  Capture-and-file skill for a Life Agent workspace. Use this whenever the user hands over
  raw input — a voice-memo transcript, messy notes, a chat/phone-call log, meeting notes,
  a stray thought — and asks to "file this", "add this", "log this", "put this where it
  belongs", "capture this", "record this", or "/add". It analyses the input and merges
  each piece into the correct workspace file, never overwriting.
---

# add — capture & file

Routes any input into the right place in the workspace, following the folder map in the
root `CLAUDE.md`. The whole point: you brain-dump, the agent files it correctly and
tells you where everything went.

---

## Step 0 — preserve the raw input (conditional)

**Only for long or multi-topic inputs** (roughly 500+ words, or 2+ distinct topics —
transcripts, meeting notes, rambling memos): save the raw text verbatim *before*
summarizing, so you can later verify nothing was dropped.

- Skip this for short single instructions ("add buy milk to my todo", "we decided on the
  blue logo") — go straight to Step 1. Don't create clutter.
- Location: `30_KNOWLEDGE/raw_inputs/YYYY-MM/YYMMDD_HHMM_topic.md`
- Format:
  ```
  ---
  date: YYYY-MM-DD HH:MM
  source: {conversation / filename / transcript}
  input_type: {text, voice-transcript, chat-log, meeting-notes}
  retention: 6 months (temporary — delete when expired, no archive)
  ---

  {the raw input, verbatim — no summarizing, editing, or omission}
  ```
- If it's a transcript, keep the transcriber's output as-is (don't fix errors here — the
  raw is the raw).
- Everything downstream (summary, routing, merge) uses this saved copy as the reference
  point. `raw_inputs/` is a temporary compare-buffer, not a permanent asset — files are
  deletable 6 months after the date in their name. Report stale ones when you notice them.

---

## Step 1 — check the input type

- **Audio file** → run the `stt` skill first to transcribe, then continue.
- **Text / notes / screenshots** → analyze directly.

> **Transcripts — required check:** proper nouns (names, companies, places) in
> speech-to-text are often wrong. Cross-check every name against `00_SELF/people/people.md`
> before recording it, and trust existing entries over a strange-looking transcribed
> spelling.

---

## Step 2 — read the content

- **Long / multi-topic** (500+ words or 2+ topics) → summarize into structured sections
  first (topic sections + source quotes + unverified items). Don't compress on the fly —
  that's how details get silently dropped.
- **Short / single instruction** → extract directly.

Then pull out:

- **People**: anyone new → candidate for `people.md`
- **Confirmed decisions** ("let's go with", "confirmed", "OK") → `decisions_log.md`
- **Rejections / taste feedback** ("not this", "no", "redo") → `feedback_patterns.md`
- **Tasks / deadlines** (dated action items) → `todo.md`
- **Self-knowledge** (the owner describing their own disposition) → `character.md`
- **Recent status / open threads** → `shared_memory.md`
- **Project or domain detail** → the relevant folder

---

## Step 3 — decide routing

| Information type | Target file |
|---|---|
| Recent issue, status update, handoff note | `00_SELF/memory/shared_memory.md` |
| Confirmed decision `[OWNER]` | `00_SELF/decisions/decisions_log.md` |
| Rejection pattern, taste filter `[OWNER]` | `00_SELF/decisions/feedback_patterns.md` |
| Task / deadline | `00_SELF/memory/todo.md` |
| New / updated person | `00_SELF/people/people.md` |
| Self-disposition, personality `[OWNER]` | `00_SELF/identity/character.md` |
| Active project (has a deadline) | `10_WORK/{project}/` |
| Ongoing role / domain | `20_DOMAINS/{domain}/` |
| Research / knowledge | `30_KNOWLEDGE/` |
| Money / family / health | `50_LIFE/` |
| Genuinely unclear | `shared_memory.md` (and flag it) |

`[OWNER]` = the owner said or confirmed it. Things you inferred are `[AI]` — keep them separate.

---

## Step 4 — show the plan before executing

Report the plan first:

```
## Update plan
| File | What I'll add | Why |
|------|---------------|-----|
| shared_memory.md | ... | ... |
| decisions_log.md | ... | ... |
```

Apply after the user OKs. If they already said "just do it", skip the plan and execute.

---

## Step 5 — execute (merge rules — apply to every file)

- **Never overwrite.** Always append/merge into existing content. Add to the matching
  section if one exists; create a new section if not.
- **Conflicts:** if new info contradicts something recorded, don't silently replace —
  tag it `[CONFLICT]` and ask.
- **Updates are additions.** For an ongoing matter, add "new fact" — don't delete the old
  record and swap in the latest. The history *is* the asset.

Per-file conventions:
- **shared_memory.md** — newest at top; header `## YYYY-MM-DD — one-line title`; bullets,
  terse; mark follow-ups with `→ needs check` / `→ waiting`.
- **decisions_log.md** — confirmed only; `- [confirmed] **decision**: reason/context`
  under a `### YYYY-MM-DD` section.
- **feedback_patterns.md** — category tag (`[tone] [brand] [strategy] [format] [taste]`)
  + always a line on *why* it was rejected and how to apply it next time.
- **todo.md** — convert relative dates ("Thursday", "next week") to absolute dates. Flag
  anything already overdue.
- **people.md** — new person → the file's format block; existing person → add
  `[YYYY-MM-DD update]` to their notes.
- **character.md** — `[OWNER]` only, things the owner actually said about themselves.

---

## Step 6 — report

```
Done:
- raw preserved — raw_inputs/YYYY-MM/YYMMDD_HHMM_topic.md
- shared_memory.md — [one-line] (merged)
- decisions_log.md — [one-line] (merged)
- people.md — [name] updated (merged)
```

End with any follow-ups (waiting on X, needs confirmation).

---

## Judgment

- **Ambiguous** → put it in `shared_memory.md`, and mirror to a better home if one exists.
- **Spans multiple files** → split it appropriately into each; don't fear a little
  duplication (important things are better in several places than lost in one).
- **New person** → stop and confirm before adding to `people.md`.
- **`[OWNER]` vs `[AI]`** → if unsure, record it but mark "needs check". Never fabricate.
