# decisions/

The owner's settled ground, in two files:

- **`decisions_log.md`** — what you've *confirmed*. Stops the agent re-opening closed
  questions.
- **`feedback_patterns.md`** — what you've *rejected*, and the general rule behind each
  rejection. Filters future proposals automatically.

Both are `[OWNER]` — only confirmed statements go here. The agent may draft entries, but
the owner is the source of truth. On any conflict with an `[AI]` inference elsewhere,
these files win.

This is the pair that makes the agent feel like it "learns" you: accepted things stop
being re-asked, rejected things stop being re-suggested.
