#!/usr/bin/env bash
# One-shot: index new conversations, then (re)start the recall API.
# Run it on a schedule (cron/launchd) to keep memory fresh. See README.
set -euo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"

echo "[1/2] indexing new conversations…"
"$PY" index_claude.py

echo "[2/2] reloading API (starting it if needed)…"
PORT="${CONVMEM_PORT:-8766}"
if curl -sf "http://127.0.0.1:${PORT}/health" >/dev/null 2>&1; then
    curl -sf -X POST "http://127.0.0.1:${PORT}/reload" >/dev/null && echo "reloaded."
else
    echo "API not running — starting in background (log: ./server.log)"
    nohup "$PY" server.py > server.log 2>&1 &
    sleep 1
    curl -sf "http://127.0.0.1:${PORT}/health" && echo " — up."
fi
