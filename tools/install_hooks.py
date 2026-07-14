#!/usr/bin/env python3
"""Safely merge this workspace's hooks into ~/.claude/settings.json.

The problem it solves: hand-editing settings.json risks clobbering hooks you already
have. This merges idempotently — it only ADDS the entries it manages, matched by command
string, and leaves everything else (other hooks, statusline, permissions) untouched.
Re-running it is a no-op.

    python3 tools/install_hooks.py            # merge (writes a .bak first)
    python3 tools/install_hooks.py --dry-run  # show what would change

By default it wires:
  - SessionStart      -> load Tier-1 memory (shared_memory.md, todo.md)
  - UserPromptSubmit  -> tools/hooks/context_gate.py  (personal-context gate)
Add conversation-memory's hook.py yourself if you set that up (see its README).
"""

import argparse
import json
import os
import shutil
import sys

SETTINGS = os.path.expanduser("~/.claude/settings.json")
WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Hooks this installer manages. cmd is matched literally to detect "already installed".
MANAGED = [
    {
        "event": "SessionStart",
        "matcher": "startup",
        "cmd": "cat 00_SELF/memory/shared_memory.md 00_SELF/memory/todo.md 2>/dev/null",
    },
    {
        "event": "UserPromptSubmit",
        "matcher": None,
        "cmd": f"python3 {os.path.join(WORKSPACE, 'tools/hooks/context_gate.py')}",
    },
]


def load_settings():
    if not os.path.exists(SETTINGS):
        return {}
    try:
        with open(SETTINGS) as f:
            return json.load(f)
    except json.JSONDecodeError:
        sys.exit(f"{SETTINGS} is not valid JSON — fix or move it, then re-run.")


def already_present(event_entries, cmd):
    for entry in event_entries:
        for h in entry.get("hooks", []):
            if h.get("command") == cmd:
                return True
    return False


def merge(settings):
    settings.setdefault("hooks", {})
    added = []
    for m in MANAGED:
        arr = settings["hooks"].setdefault(m["event"], [])
        if already_present(arr, m["cmd"]):
            continue
        entry = {"hooks": [{"type": "command", "command": m["cmd"]}]}
        if m["matcher"]:
            entry["matcher"] = m["matcher"]
        arr.append(entry)
        added.append(f"{m['event']}: {m['cmd']}")
    return added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    settings = load_settings()
    # work on a copy for dry-run reporting
    import copy
    added = merge(copy.deepcopy(settings) if args.dry_run else settings)

    if not added:
        print("Nothing to do — managed hooks already present.")
        return
    print("Will add:" if args.dry_run else "Added:")
    for a in added:
        print(f"  + {a}")

    if args.dry_run:
        return

    os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
    if os.path.exists(SETTINGS):
        shutil.copy(SETTINGS, SETTINGS + ".bak")
        print(f"\nBackup: {SETTINGS}.bak")
    with open(SETTINGS, "w") as f:
        json.dump(settings, f, indent=2)
    print(f"Wrote: {SETTINGS}")
    print("Note: SessionStart runs relative to your workspace — launch Claude Code from"
          " the workspace root, or make the cat paths absolute.")


if __name__ == "__main__":
    main()
