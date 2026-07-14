# Update — pull framework improvements without losing your life

This workspace separates the **framework** (routers, docs, skills, tools — tracked and
improved over time) from **your data** (identity, people, decisions, memory — git-ignored,
never touched by an update). That separation is what makes updates safe: you can pull new
framework versions and your personal content stays exactly as it is.

## One-time setup: point at the upstream template

If you cloned/forked this template, add the original as an `upstream` remote once:

```bash
git remote add upstream https://github.com/ORIGINAL-OWNER/ORIGINAL-REPO.git
```

(Replace with the template's URL. Your own repo stays `origin`.)

## Pulling an update

```bash
git fetch upstream
git merge upstream/main        # or: git rebase upstream/main
```

- **Your live data files won't conflict** — they're git-ignored, so upstream doesn't track
  them. Only framework files and the `*.example` seeds move.
- **New seeds** (`*.example`) arrive without overwriting your live files. Run
  `bash tools/bootstrap.sh` again — it only creates files that don't exist yet, so it fills
  in any *new* pieces and skips everything you already have.
- **If a seed improved** and you want the new version, diff it into your live file by hand:
  `diff 00_SELF/identity/character.md.example 00_SELF/identity/character.md`.
- **The one file that can conflict is the root `CLAUDE.md`** (you filled a few tokens in
  it). If git flags a conflict there, keep your name/timezone/language lines and take
  upstream's changes to everything else — or just ask the agent: *"resolve the CLAUDE.md
  merge conflict, keep my personal tokens, take upstream's structure."*

## Let the agent do it

> **"Update the framework from upstream per UPDATE.md, keep all my personal data, and tell
> me what changed."**

The agent fetches, merges framework-only, re-runs bootstrap for new seeds, and summarizes
the diff — your data untouched.
