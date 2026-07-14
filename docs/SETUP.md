# Setup — from clone to your own agent

No coding needed. Budget 20–30 minutes for a first pass; the rest fills in as you use it.

## Step 0 — prerequisites

- [Claude Code](https://claude.com/claude-code) installed
- A place to keep this workspace (any folder; a cloud-synced folder like iCloud/Dropbox/
  Google Drive works well so your agent's memory follows you across machines)

## Step 1 — get your own copy and open it

Recommended: on the GitHub page click **"Use this template" → create a PRIVATE
repository** (this workspace will hold your life — private is the right default), then
clone *yours*. Just trying it out? Cloning the original directly also works.

```bash
git clone https://github.com/YOUR-USERNAME/my-workspace.git my-workspace
cd my-workspace
claude
```

When you run `claude`, you land in a chat prompt (`>`). You talk to it in plain
language — **any language, including yours.** That's the whole interface.

### How do I actually edit these files? (three ways, easiest first)

You don't need to be a coder. Pick whichever feels comfortable:

1. **Just ask the agent** (easiest). In Claude Code, say: *"Open CLAUDE.md and fill in
   my name, timezone, and language — I'll tell you the values."* It edits the file for you.
2. **Any text editor.** These are plain text files. Open the folder in VS Code, or open a
   single file with TextEdit / Notepad. Edit, save.
3. **Terminal**, if you like it: `nano CLAUDE.md`.

### Is this safe? Can I undo?

Yes. Two safety nets:
- Claude Code **shows you each change and asks before applying it** (unless you turn that
  off). Nothing happens behind your back.
- This folder is a **git repository**, which means every version is saved. If anything
  goes wrong, tell the agent *"undo the last change with git"* and it will. You never have
  to learn git yourself.

## Step 1.5 — bootstrap your private files

```bash
bash tools/bootstrap.sh
```

This copies each `*.example` seed to its real filename (`character.md.example` →
`character.md`). Those live files are **git-ignored**, so your data is private by default —
you can even make your fork public without leaking anything (that's why there's no manual
"untrack" step anymore). The onboarding agent runs this for you; you only need it if you're
going by hand. See [UPDATE.md](../UPDATE.md) for how framework updates leave these untouched.

## Step 2 — let the agent onboard you

The fastest path is to just say:

> **"Set this up for me."**

That's the trigger. The agent runs `ONBOARDING.md` — an interview script that doesn't
just fill in your name, but reshapes the workspace to *your* actual life: your roles,
your domains, and the answer-gate contexts. It asks one question at a time, shows you each
draft, and waits for your OK. You can stop after the identity step and start using it; the
rest can happen later. If you'd rather do it by hand, continue below.

## Step 3 — fill the center (`00_SELF`)

> **Minimum to start today:** write 5 honest lines in `character.md`. That's it. You can
> literally stop after that and start using it. Everything below is "fill it in as you go."

This is the only part that matters on day one. Everything else is optional.

1. **`00_SELF/identity/character.md`** — who you are. Don't overthink it. Five honest
   lines beat a perfect essay. More is fine too — the agent won't get confused by detail,
   it gets confused by *contradiction*, so just be consistent. Read before any taste call.
2. **`00_SELF/people/people.md`** — *add people as they come up, not all at once.* You do
   **not** need to fill this today. Leaving it empty is fine — the agent just asks "who's
   that?" the first time someone new appears, and you tell it. Follow the format block at
   the top of the file when you do add someone.
3. **`00_SELF/memory/agent_brain/USER.md`** — how you like to be communicated with
   (tone, length, what annoys you).

Leave `character_ai_mirror.md`, `decisions_log.md`, and `feedback_patterns.md` mostly
empty — the agent fills those as you work.

## Step 4 — wire the hooks (optional — one command)

> **Not a coder? You can skip this whole step.** The workspace works without hooks — you'd
> just say "read my shared_memory and todo" at the start of a session instead of it being
> automatic.

Two hooks make the workspace feel alive: a **SessionStart** hook that auto-loads your
recent context (Tier-1 memory), and a **UserPromptSubmit** context-gate that enforces the
answer gate's core rule ("personal context → public-persona OFF", `docs/CONVENTIONS.md`
§3–4) — prose alone gets diluted in long sessions, a hook doesn't.

Rather than hand-edit JSON, run the installer — it **merges** into `~/.claude/settings.json`
without clobbering anything you already have (idempotent; re-running is a no-op):

```bash
python3 tools/install_hooks.py --dry-run   # preview
python3 tools/install_hooks.py             # apply (writes a .bak first)
```

Or just ask the agent: *"install my workspace hooks."* Before relying on the context gate,
open `tools/hooks/context_gate.py` and adjust `KEYWORDS` to your language and life (the
defaults are English; there's a Korean example in the file).

> Note: the SessionStart hook uses workspace-relative paths, so launch Claude Code from the
> workspace root (or make those paths absolute in `settings.json`).

## Step 5 — start using it

Just talk to it. As you do:
- decisions you confirm → the agent logs them in `decisions_log.md`
- things you reject → it files the reason in `feedback_patterns.md`
- patterns it notices in you (2+ times) → `character_ai_mirror.md`
- projects with deadlines → a folder in `10_WORK/` (copy `_PROJECT_TEMPLATE/`)
- ongoing roles → a folder in `20_DOMAINS/` (copy `_DOMAIN_TEMPLATE/`)

## Step 6 — your data is private by default

Good news: **there's nothing to do here.** This template ships personal files as
`*.example` seeds; `bootstrap.sh` copies them to live filenames that are **git-ignored**
(see `.gitignore`). So your identity, people, decisions, and memory are never tracked and
never published — even if your copy is public. Framework files stay tracked so you can pull
updates ([UPDATE.md](../UPDATE.md)) without touching your data.

Two habits still worth keeping:
- **Prefer a private repo anyway.** Belt and suspenders — your life doesn't need to be on
  a public URL at all.
- **If you ever add a genuinely secret value**, put it in `.env` (already git-ignored),
  never in a tracked `.md`. And if personal data was *ever* pushed publicly at some point,
  treat it as leaked — flipping a repo private later doesn't erase forks or caches.

## Step 7 — optional power-ups

Once the center is filled and you're using it daily, these are worth adding:

- **The `add` skill** — brain-dump anything (notes, a transcript, a chat log) and the
  agent files each piece into the right place. `ln -s "$(pwd)/skills/add"
  ~/.claude/skills/add`, or ask the agent to install it. See [`skills/README.md`](skills/README.md).
- **The `stt` skill** — transcribe voice memos (needs a free Deepgram key), then hand the
  text to `add`.
- **Conversation memory** — let the agent recall relevant past chats automatically. It's a
  small local service; the agent can build it with you: *"set up conversation-memory from
  extras/conversation-memory — walk me through it."* See
  [`extras/conversation-memory/README.md`](../extras/conversation-memory/README.md).

## Monthly maintenance (5 minutes)

Structure decays silently unless something shrinks it. Once a month:

1. **Roll old memory**: `python3 tools/split_shared_memory.py --dry-run`, review, then run
   it for real. Keeps every session's always-loaded context lean.
2. **Sweep 10_WORK**: any project silent for 2–3 months? Decide its status honestly
   (see `10_WORK/CLAUDE.md`, "stale-project sweep") and archive what's done.
3. **Re-check the line budget**: root `CLAUDE.md` still ≤ 200 lines? Any rule now
   duplicated in two places? (`docs/CONVENTIONS.md` §10)

Or just tell the agent: *"run the monthly maintenance from SETUP.md"*.

## What NOT to do

- Don't put API keys or passwords in any `.md` file. Use `.env` (already gitignored).
- Don't try to fill every folder on day one. The structure rewards gradual accretion.
- Don't delete the `_TEMPLATE` folders — they're your copy-me scaffolds.

## Optional: a second, isolated agent (`90_SHARED`)

If you want an agent you share with a partner or family — one that can see shared plans
but **not** your private `00_SELF` — that's what `90_SHARED/` is for. Its `CLAUDE.md`
hard-restricts access to that folder only. Run it as a separate Claude Code session or
sandbox. Delete the folder if you don't need it.
