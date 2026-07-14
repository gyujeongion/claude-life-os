"""Shared helpers: config, embeddings, noise filtering."""

import os
import re
import struct
import urllib.request
import json

# --- config (override via environment) ---------------------------------------
DB_PATH = os.environ.get("CONVMEM_DB", os.path.expanduser("~/.conversation-memory/conv.db"))
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
# bge-m3 is multilingual and works well for non-English queries. nomic-embed-text is
# faster but fails on some non-English queries — don't use it if you think in another
# language. Whatever you pick, index and query MUST use the same model.
EMBED_MODEL = os.environ.get("CONVMEM_EMBED_MODEL", "bge-m3")
API_PORT = int(os.environ.get("CONVMEM_PORT", "8766"))
MAX_CHARS = 2400  # truncate very long turns before embedding

# Retrieval gate thresholds. These defaults were tuned on one corpus — they are a
# STARTING POINT, not universal. Cosine ranges shift with embedding model, language, and
# chunk length, so re-tune on a small labelled query set for your own data (README).
GATE = {
    "ABS_MIN": float(os.environ.get("CONVMEM_ABS_MIN", "0.54")),   # never inject below this
    "TOP1_MIN": float(os.environ.get("CONVMEM_TOP1_MIN", "0.62")),  # below = "weak" distribution
    "GAP": float(os.environ.get("CONVMEM_GAP", "0.10")),            # drop results this far under top1
    "STRONG_MAX": int(os.environ.get("CONVMEM_STRONG_MAX", "3")),
    "WEAK_MAX": int(os.environ.get("CONVMEM_WEAK_MAX", "1")),
}


def connect(path=None):
    """Open the DB with sane concurrency defaults (WAL + a busy wait)."""
    import sqlite3
    conn = sqlite3.connect(path or DB_PATH, timeout=5.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn

# --- noise filter ------------------------------------------------------------
# Machine-generated wrappers that pollute a semantic index. Extend for your setup.
_NOISE_RE = re.compile(
    r"(system-reminder|<task-notification|tool_use_id|Background command|"
    r"session (was )?continued|Caveat: The messages below|"
    r"This is an automated|hookSpecificOutput)",
    re.IGNORECASE,
)


def is_noise(text: str) -> bool:
    t = (text or "").strip()
    if len(t) < 12:
        return True
    return bool(_NOISE_RE.search(t))


def strip_wrappers(text: str) -> str:
    """Peel common wrappers so the real utterance gets embedded, not the envelope."""
    t = re.sub(r"\[Image #\d+\]", "", text or "")
    t = re.sub(r"<[^>]{1,40}>", "", t)  # short xml-ish tags
    return t.strip()


# --- embeddings --------------------------------------------------------------
def embed(text: str) -> list[float]:
    """One embedding via Ollama. Raises on failure (indexer should handle/retry)."""
    body = json.dumps({"model": EMBED_MODEL, "prompt": text[:MAX_CHARS]}).encode()
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/embeddings", data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["embedding"]


def pack(vec: list[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def unpack(blob: bytes) -> list[float]:
    return list(struct.unpack(f"{len(blob) // 4}f", blob))
