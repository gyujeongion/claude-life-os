# conversation-memory — the agent that remembers your past chats

An optional add-on for the Life Agent workspace. It gives your agent **semantic recall of
your own past conversations**: when something you're saying now is related to a chat you
had weeks ago — even in a different session — the relevant bit gets pulled back into
context automatically.

> This is different from the workspace's markdown memory (`shared_memory.md` etc.), which
> the agent *curates by hand*. This one indexes **everything** you've said to Claude Code
> and retrieves by meaning. They complement each other.

**Honest expectations.** This is a compact reference implementation — a few hundred lines
you fully own and can read in one sitting. It is not a hosted product. It runs locally,
uses your own machine's compute, and stores everything in one SQLite file. No data leaves
your computer.

---

## How it works (five moving parts)

```
  ~/.claude/projects/**/*.jsonl        (Claude Code writes these automatically)
            │
            ▼  index_claude.py   — extract turns, filter noise, embed (Ollama), store
      conv.db  (SQLite: text + float32 embeddings)
            │
            ▼  server.py         — load vectors into RAM, cosine search + retrieval gate
      http://127.0.0.1:8766/recall
            │
            ▼  hook.py           — UserPromptSubmit hook: inject relevant past turns
      your next Claude Code prompt, now with memory
```

Files:
- `index_claude.py` — reads your Claude Code logs, embeds new turns incrementally.
- `server.py` — tiny stdlib HTTP API: `/recall`, `/health`, `/reload`.
- `hook.py` — the Claude Code hook that injects recalled turns (fails silently).
- `common.py` — config + embeddings + noise filter.
- `run.sh` — index-then-reload; run on a schedule to keep it fresh.

**Two design decisions worth knowing** (learned the hard way, baked into the code):
1. **The retrieval gate judges the *shape* of the score distribution, not one threshold.**
   A single cutoff can't separate a genuinely relevant memory (cosine 0.54) from unrelated
   small-talk (0.56). `server.py` uses a floor + a top-1 test + a gap test instead. This is
   the difference between "spookily good recall" and "random noise in every prompt."
2. **The injection is framed as *maybe irrelevant*.** `hook.py` prepends a header telling
   the agent to confirm intent from the current request first and treat recall as
   secondary. Fuzzy retrieval + an over-trusting reader = confidently wrong answers.

---

## Prerequisites

- [Ollama](https://ollama.com) running locally, with an embedding model pulled:
  ```bash
  ollama pull bge-m3
  ```
  (bge-m3 is multilingual and a safe default. In our testing, `nomic-embed-text`
  separated non-English queries poorly — if you converse in another language, evaluate
  before switching. Whatever you pick, index and query must use the **same** model; if you
  change it later, re-index from scratch.)
- Python 3.9+ with `numpy` and `requests` (`pip install -r requirements.txt`).

---

## Build it with the agent (recommended)

You don't have to do this by hand. Open Claude Code in your workspace and say:

> **"Set up conversation-memory from extras/conversation-memory — walk me through it."**

A capable agent will follow the steps below, checking each one with you. Point it at this
section if it needs the script.

### Agent runbook

1. **Check prerequisites.** `ollama --version`; `ollama list | grep bge-m3` (pull if
   missing); `python3 -c "import numpy, requests"` (else `pip install -r requirements.txt`).
2. **First index.** `python3 index_claude.py`. This can take a while the first time (it
   embeds every past turn). Report the chunk count.
3. **Start the API — durably.** `bash run.sh` starts the server with `nohup` if it isn't
   already up (a bare `python3 server.py &` dies when the shell closes). Then
   `curl -s localhost:8766/health` should show `{"ok": true, "chunks": N}`. For a
   permanent service, wrap `run.sh`/`server.py` in launchd (macOS) or systemd (Linux).
4. **Smoke-test recall.** `curl -s "localhost:8766/recall?q=<something the user actually
   discussed before>&limit=3"` and show the results. If they're relevant, the gate is
   working. If everything comes back empty, either the query has no match (try a topic you
   know is in there) or the gate thresholds need tuning for your corpus — see "Tuning".
5. **Wire the hook.** Merge into `~/.claude/settings.json` — **don't clobber existing
   hooks**; if a `UserPromptSubmit` array is already there (e.g. the workspace's
   `context_gate.py`), append this as another entry in the same array. Confirm before
   writing:
   ```json
   { "hooks": { "UserPromptSubmit": [ { "hooks": [
       { "type": "command", "command": "python3 /ABS/PATH/extras/conversation-memory/hook.py" }
   ] } ] } }
   ```
   Use the real absolute path.
6. **Schedule freshness.** The server only sees what's indexed *and loaded*. `run.sh` does
   both (index new turns, then `POST /reload`) — add it to cron
   (`*/30 * * * * /abs/path/extras/conversation-memory/run.sh`) or a launchd/systemd timer.
   If you ever run `index_claude.py` by hand, remember to `curl -X POST
   localhost:8766/reload` after, or the API won't see the new rows. Tradeoff: more frequent
   = fresher memory, slightly more CPU.
7. **Confirm the loop.** Start a fresh Claude Code session, mention something from an old
   chat, and check that a `[recalled past conversation]` block appears. Done.

### Do it by hand

```bash
pip install -r requirements.txt
ollama pull bge-m3
python3 index_claude.py          # first index (slow once)
python3 server.py &              # start API
curl -s localhost:8766/health    # {"ok": true, "chunks": N}
# add hook.py to ~/.claude/settings.json (see step 5)
# add run.sh to cron for freshness (see step 6)
```

---

## Config (environment variables)

| Var | Default | Meaning |
|---|---|---|
| `CONVMEM_DB` | `~/.conversation-memory/conv.db` | where the store lives |
| `OLLAMA_URL` | `http://localhost:11434` | embedding backend |
| `CONVMEM_EMBED_MODEL` | `bge-m3` | embedding model (must match index & query) |
| `CONVMEM_PORT` | `8766` | API port |

---

## Privacy & threat model (read this)

- **Local only.** The API binds `127.0.0.1` — it is not exposed to your network. Everything
  (logs, DB, embedding model) stays on your machine. Nothing is sent anywhere.
- **No authentication, by design.** The API is unauthenticated because it only listens on
  localhost for a single user. That means *any process running as you* can query your
  conversation history on port 8766. On a shared or untrusted machine, that's a real
  exposure — don't run it there, or firewall the port. Never change the bind address to
  `0.0.0.0`.
- **The DB is plaintext.** `~/.conversation-memory/conv.db` holds your conversations
  verbatim, unencrypted. Treat the folder like any sensitive data; it's outside the repo
  by default — don't commit it. Delete it to forget everything.
- **Recalled text is untrusted input.** Injected snippets are *data about past
  conversations*, not commands — the hook header says so explicitly, so a stray imperative
  in your own logs can't hijack the agent. Keep that header if you edit the hook.
- **Scope.** This indexes Claude Code logs. Adapt `index_claude.py` for other sources
  (it's small and commented) — the store and API don't care where chunks come from.

## Tuning the gate (do this if recall feels off)

The thresholds in `common.py` (`GATE`, all env-overridable) were tuned on one corpus.
Cosine ranges shift with embedding model, language, and how long your turns are, so treat
them as a starting point:

- **Recall injects noise / unrelated stuff** → raise `CONVMEM_ABS_MIN` (e.g. 0.58) and/or
  `CONVMEM_TOP1_MIN`.
- **Recall never fires even for clearly related topics** → lower them.
- **Right topic, but too many/few snippets** → adjust `CONVMEM_GAP` and `CONVMEM_STRONG_MAX`.

The honest way to set these: save ~10 real queries you know the answer to, label which
past chunks *should* come back, and sweep the thresholds against that set. A single
"correct" number doesn't exist across languages — verify on your own data.

## Extending (pointers, not built in)

Kept out to stay minimal; add if you need them:
- **Recency weighting** — decay old chunks in scoring so stale topics sink.
- **A reranker** — a cross-encoder over the top-k lifts precision on weak matches (run it
  on CPU; sharing a GPU with Ollama can deadlock).
- **Soft-archive of dead topics** — mark abandoned threads `status='noise'` instead of
  deleting, so recall skips them but nothing is lost.
