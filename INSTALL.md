# Install

The whole point: **you give this to your AI and it sets itself up.** No coding.

## The one prompt

Get your own copy first — on GitHub click **"Use this template" → create a PRIVATE
repository** (it will hold your life), then clone it and open Claude Code in the folder:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git my-workspace
cd my-workspace
claude
```

Then paste this single prompt:

> **"Read INSTALL.md and set up this workspace for me — run bootstrap, then onboard me,
> and offer to wire the hooks. Ask before touching anything outside this folder."**

That's it. The agent does the rest, checking with you at each step.

## What the agent does (and what you'd do by hand)

1. **Bootstrap your private files.** `bash tools/bootstrap.sh` — copies every `*.example`
   seed to its live filename. Those live files are git-ignored, so **your data is private
   by default** and never gets committed. (Framework files stay tracked so you can pull
   updates later — see [UPDATE.md](UPDATE.md).)
2. **Onboard.** The agent runs [`ONBOARDING.md`](ONBOARDING.md) — an interview that shapes
   the workspace to your actual life (roles, domains, the answer-gate contexts). One
   question at a time, every draft shown for your OK. You can stop after the identity step.
3. **Wire the hooks (optional).** `python3 tools/install_hooks.py` merges the auto-load and
   context-gate hooks into `~/.claude/settings.json` **without clobbering** anything you
   already have (it's idempotent; `--dry-run` to preview). Skip if you're not ready.

## Prerequisites

- [Claude Code](https://claude.com/claude-code) (or any capable agent harness).
- A private repo/folder to keep it in. A cloud-synced folder (iCloud/Dropbox/Drive) means
  your agent's memory follows you across machines.
- Nothing else to start. The `stt` skill and conversation-memory add-on have their own
  (optional) requirements — see [`skills/`](skills/) and
  [`extras/conversation-memory/`](extras/conversation-memory/).

Full manual walkthrough → [`docs/SETUP.md`](docs/SETUP.md) · Korean → [`docs/QUICKSTART.ko.md`](docs/QUICKSTART.ko.md)
