# ONBOARDING.md — agent-run setup script

> **This file is for the AI agent, not the human.** When a user opens this workspace and
> says something like *"set this up for me"* — or whenever `{{PLACEHOLDER}}` tokens are
> still present anywhere — the agent runs this script to turn the generic template into a
> workspace tailored to *this specific person's* life and domains.
>
> 이 파일은 사람이 아니라 AI 에이전트용입니다. 사용자가 "이대로 세팅해줘"라고 하거나
> `{{PLACEHOLDER}}`가 남아있으면, 에이전트가 이 스크립트를 실행해 제네릭 템플릿을 그
> 사람의 삶·도메인에 맞춘 워크스페이스로 바꿉니다.

---

## Rules for the agent running this

1. **Interview, one question at a time.** Do not dump all questions at once. Wait for each
   answer. Mirror the user's language.
2. **Adapt, don't just fill.** The goal is not to paste a name into `{{OWNER_NAME}}`. It's
   to reshape the A–G contexts, domains, and axis to match how *this* person actually lives.
3. **Draft, then confirm.** After each section, show what you wrote and get a yes before
   moving on. Everything is reversible (git) — say so if the user hesitates.
4. **Never invent facts.** If the user doesn't answer something, leave it as a clearly
   marked TODO. Don't fabricate a personality.
5. **Minimum viable exit.** The user can stop after Step 2 (identity). Tell them that. The
   rest can happen later, on demand.

---

## Step 0 — Bootstrap private files (do this first, silently)

Before interviewing, run `bash tools/bootstrap.sh`. It copies each tracked `*.example`
seed to its live filename (e.g. `character.md.example` → `character.md`). The live files
are git-ignored — this is what keeps the user's data private by default. It only creates
missing files, so it's safe. Then interview against the **live** files, never the
`.example` seeds. Mention in one line that you did it; don't belabor it.

## Step 1 — Basics (fills `CLAUDE.md`, `agent_brain/MEMORY.md`)

Ask, in order:
- "What should I call you?" → `{{OWNER_NAME}}`
- "What timezone are you in?" → `{{TIMEZONE}}`
- "What language should I speak with you?" → `{{PRIMARY_LANGUAGE}}`
- "In one line, what do you do?" → the "what they do" fields

Then replace every matching `{{...}}` token across `CLAUDE.md` and
`00_SELF/memory/agent_brain/MEMORY.md`. Confirm.

## Step 2 — Identity (fills `00_SELF/identity/character.md`, `agent_brain/USER.md`)

Interview for `character.md`:
- "How do you make decisions — fast and intuitive, or slow and analytical?"
- "What are the 3–5 things that actually matter to you? Be specific."
- "What's your taste — what are you drawn to, what repels you?"
- "Any hard red lines — things I should never do or suggest?"

Interview for `USER.md`:
- "How do you want me to talk to you — blunt or gentle? short or thorough?"
- "What makes you trust a response? What makes you distrust one?"
- "What should I just do vs. always check with you first?"

Draft both files from the answers. Show them. Confirm.

> **This is the minimum.** After this, tell the user: *"That's enough to start — you can
> stop here and just talk to me, or keep going to tailor the domains and router."*

## Step 3 — Domains (the part that makes it *theirs*)

This is what turns a generic template into a personal one. Ask:

- "What are the ongoing roles or hats you wear? (a job, a side business, a craft, a
  community you run — things with no end date)"

For each role the user names:
- copy `20_DOMAINS/_DOMAIN_TEMPLATE/` → `20_DOMAINS/{ROLE_NAME}/`
- fill that folder's `CLAUDE.md` with the role's specifics (how to handle its questions,
  where its documents go)

Then ask:
- "Anything you're actively working on that has a deadline?" → for each, copy
  `10_WORK/_PROJECT_TEMPLATE/` → `10_WORK/{PROJECT}/` and fill its `README.md`.

## Step 4 — Tailor the answer gate (`00_SELF/context_router.md`)

The template ships with generic A–G contexts. **Rewrite them to match this person's
actual life areas**, using what you learned in Steps 2–3. Examples of how they might
differ per person:
- an illustrator: A = client work, B = personal art, C = taste, F = relationships…
- a founder: A = the company, B = fundraising, E = personal finance, F = team/relationships…
- a student: A = studies, C = taste, D = life transitions, F = relationships…

Keep the **mechanism** identical (classify → switch layers → declare) and keep the one
hard rule: **L1 (public-persona/brand) is forced OFF for personal, relationship,
investment, and health contexts.** Only the labels and triggers change.

Confirm the rewritten context table with the user.

## Step 5 — Core axis (optional, `00_SELF/memory/SYNC_AXIS.md`)

Ask: "Is there a north-star principle — one sentence — that everything you do should
serve?" If yes, write it into `SYNC_AXIS.md`. If the user shrugs, skip it; it can be added
any time.

## Step 6 — Wrap up

- **Privacy check first**: ask whether their copy of this repo is private (it should
  be — it now contains their life). If they ever plan to publish it, point them to
  `docs/SETUP.md` Step 6 (the untrack procedure) and offer to run it for them.
- List what you created/changed (files + new domain folders).
- Point out that `people.md`, `decisions_log.md`, and `feedback_patterns.md` fill in
  naturally as they use it — no action needed now.
- Offer to set up the SessionStart auto-load hook (see `docs/SETUP.md` Step 4), and say
  it's fine to skip.
- Tell them: everything is in git; "undo the last change" works any time.

---

## Verify before finishing

- [ ] No `{{PLACEHOLDER}}` tokens remain in `CLAUDE.md` or `agent_brain/MEMORY.md`.
- [ ] `character.md` and `USER.md` reflect real answers, not template prompts.
- [ ] `context_router.md` contexts describe *this person's* life, not the generic example.
- [ ] Every domain the user named has a folder under `20_DOMAINS/`.
- [ ] Nothing was fabricated; unanswered items are marked TODO.
