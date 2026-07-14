# Uninstall

Nothing here is sticky. Removal is fully in your hands.

## Remove the hooks

If you ran `tools/install_hooks.py`, it left a backup:

```bash
# restore the settings you had before
mv ~/.claude/settings.json.bak ~/.claude/settings.json
```

Or edit `~/.claude/settings.json` and delete just the two entries it added (the
`cat …/shared_memory.md …` SessionStart hook and the `context_gate.py` UserPromptSubmit
hook). Everything else you had is untouched.

If you also set up **conversation-memory**, stop its service and remove its hook line from
`settings.json`, then delete its data: `rm -rf ~/.conversation-memory` and any cron/launchd
timer you added. See its README.

## Remove the skills

```bash
rm ~/.claude/skills/add ~/.claude/skills/stt   # symlinks, or -rf if you copied them
```

## Remove the workspace

It's just a folder. Your data lives in the git-ignored live files inside it, nowhere else.

```bash
rm -rf /path/to/your-workspace
```

That deletes everything — framework and your personal content. If you want to keep your
data but drop the framework, copy out the live files first (`character.md`, `people.md`,
`decisions_log.md`, `shared_memory.md`, `todo.md`, and `00_SELF/memory/projects/*.md`).

No background processes, no system changes, no residue beyond what's listed above.
