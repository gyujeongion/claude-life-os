#!/usr/bin/env python3
"""Index Claude Code conversation logs into the memory store.

Claude Code writes every session as JSONL under ~/.claude/projects/**/*.jsonl.
This walks those files, extracts substantive user/assistant turns, embeds them, and
upserts into the SQLite store. Incremental: a file is re-read only if its mtime changed.

Usage:
    python3 index_claude.py                 # index ~/.claude/projects
    python3 index_claude.py --root PATH     # index a different logs dir
    python3 index_claude.py --reset         # wipe markers and re-index everything
"""

import argparse
import glob
import json
import os
import sqlite3
import sys

import common as c


def init_db(conn):
    schema = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema) as f:
        conn.executescript(f.read())


def extract_text(message) -> str:
    """A Claude Code message content is either a string or a list of blocks."""
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "\n".join(parts)
    return ""


def turns_from_file(path):
    """Yield (seq, role, text, ts, session, cwd) for substantive turns in one session."""
    seq = 0
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            role = obj.get("type")
            if role not in ("user", "assistant"):
                continue
            msg = obj.get("message") or {}
            raw = extract_text(msg)
            if c.is_noise(raw):          # detect noise on the ORIGINAL, before stripping
                continue
            text = c.strip_wrappers(raw)
            if not text or len(text) < 12:
                continue
            yield (
                seq, role, text,
                obj.get("timestamp", ""),
                obj.get("sessionId", ""),
                obj.get("cwd", ""),
            )
            seq += 1


def index_file(conn, path, source="claude-code"):
    key = f"{source}:{path}"
    mtime = os.path.getmtime(path)
    row = conn.execute("SELECT marker FROM index_state WHERE source_key=?", (key,)).fetchone()
    if row and abs(row[0] - mtime) < 1e-6:
        return 0  # unchanged

    added = 0
    for seq, role, text, ts, session, cwd in turns_from_file(path):
        exists = conn.execute(
            "SELECT 1 FROM chunks WHERE source=? AND session_id=? AND seq=?",
            (source, session, seq),
        ).fetchone()
        if exists:
            continue
        try:
            vec = c.embed(text)
        except Exception as e:
            print(f"  embed failed ({e}); stopping this file, will retry next run", file=sys.stderr)
            break
        conn.execute(
            "INSERT OR IGNORE INTO chunks(source, session_id, seq, role, text, ts, cwd, embedding)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (source, session, seq, role, text, ts, cwd, c.pack(vec)),
        )
        added += 1

    conn.execute(
        "INSERT INTO index_state(source_key, marker) VALUES(?,?) "
        "ON CONFLICT(source_key) DO UPDATE SET marker=excluded.marker",
        (key, mtime),
    )
    conn.commit()
    return added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.expanduser("~/.claude/projects"))
    ap.add_argument("--reset", action="store_true")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(c.DB_PATH), exist_ok=True)
    conn = c.connect()
    init_db(conn)
    if args.reset:
        conn.execute("DELETE FROM index_state")
        conn.commit()

    files = sorted(glob.glob(os.path.join(args.root, "**", "*.jsonl"), recursive=True))
    if not files:
        print(f"No .jsonl logs under {args.root}")
        return

    total = 0
    for i, path in enumerate(files, 1):
        n = index_file(conn, path)
        total += n
        if n:
            print(f"[{i}/{len(files)}] +{n}  {os.path.basename(path)}")
    print(f"\nDone. {total} new chunks. DB: {c.DB_PATH}")
    conn.close()


if __name__ == "__main__":
    main()
