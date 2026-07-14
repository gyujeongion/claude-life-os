# skills/ — optional Claude Code skills for this workspace

These are [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills) that
make the Life Agent workspace nicer to live in. They're **optional** — the workspace works
without them — but they're the tools the template author reaches for daily.

| Skill | What it does | Needs |
|---|---|---|
| [`add`](add/SKILL.md) | "Just file this for me." Takes any dump — a voice memo, messy notes, a chat log — and routes each piece into the right workspace file, without overwriting anything. | nothing (uses the folder structure) |
| [`stt`](stt/SKILL.md) | Transcribe an audio file to text (speaker-labelled). Feeds naturally into `add`. | a [Deepgram](https://deepgram.com) API key (free tier) |

## Install (once)

Claude Code loads skills from `~/.claude/skills/`. Symlink these so updates to your
workspace stay in sync:

```bash
# from your workspace root
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/add" ~/.claude/skills/add
ln -s "$(pwd)/skills/stt" ~/.claude/skills/stt
```

Or just tell the agent: *"install the add and stt skills from ./skills into ~/.claude/skills"*.

Prefer to copy instead of symlink? `cp -r skills/add ~/.claude/skills/` works too — you
just won't get updates automatically.

## Related: conversation memory

There's a bigger, optional add-on in [`../extras/conversation-memory/`](../extras/conversation-memory/) —
a self-hosted semantic memory that lets the agent recall relevant *past conversations*
automatically. It's more involved to set up (a background service), so it lives separately.
The agent can build it with you step by step.
