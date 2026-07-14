#!/usr/bin/env python3
"""Semantic recall API for conversation memory. Zero web framework (stdlib only).

Loads all active embeddings into a numpy matrix at startup, serves cosine search over
HTTP. The retrieval gate is the important part — see recall().

    GET  /recall?q=...&limit=3   -> {"results": [{text, score, role, ts, weak}], ...}
    GET  /health                 -> {"ok": true, "chunks": N}
    POST /reload                 -> re-read the DB after indexing

    python3 server.py            # listens on CONVMEM_PORT (default 8766)
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

import numpy as np

import common as c

# The hard-won lesson (thresholds live in common.GATE, env-overridable): you cannot
# separate relevant from irrelevant with a single absolute threshold — a genuinely
# relevant memory can score 0.54 while unrelated small-talk scores 0.56. Judge the SHAPE
# of the score distribution instead. Re-tune GATE for your own corpus/language.
MAX_LIMIT = 10


class Store:
    def __init__(self):
        self.lock = threading.Lock()
        self.load()

    def load(self):
        conn = c.connect()
        rows = conn.execute(
            "SELECT id, text, role, ts, embedding FROM chunks WHERE status='active'"
        ).fetchall()
        conn.close()
        # Guard against mixed embedding dimensions (e.g. after changing the embed model)
        # or a corrupt row — drop the odd ones out instead of crashing the whole server.
        vecs, meta = [], []
        dim = None
        skipped = 0
        for r in rows:
            v = c.unpack(r[4])
            if dim is None:
                dim = len(v)
            if len(v) != dim:
                skipped += 1
                continue
            vecs.append(v)
            meta.append((r[0], r[1], r[2], r[3]))
        if skipped:
            print(f"[warn] skipped {skipped} rows with mismatched embedding dim "
                  f"(re-index if you changed the embed model)")
        self.meta = meta
        if vecs:
            mat = np.array(vecs, dtype=np.float32)
            norms = np.linalg.norm(mat, axis=1, keepdims=True)
            self.mat = mat / np.clip(norms, 1e-8, None)
        else:
            self.mat = np.zeros((0, 1), dtype=np.float32)

    def recall(self, query, limit):
        limit = max(1, min(int(limit), MAX_LIMIT))  # clamp: a negative limit must not leak rows
        g = c.GATE
        with self.lock:
            if len(self.meta) == 0:
                return []
            q = np.array(c.embed(query), dtype=np.float32)
            q /= max(float(np.linalg.norm(q)), 1e-8)
            scores = self.mat @ q
            order = np.argsort(-scores)
            top1 = float(scores[order[0]])
            if top1 < g["ABS_MIN"]:
                return []

            weak = top1 < g["TOP1_MIN"]
            cap = min(limit, g["WEAK_MAX"] if weak else g["STRONG_MAX"])
            out = []
            for idx in order[:cap]:
                s = float(scores[idx])
                if s < g["ABS_MIN"]:
                    break
                if not weak and (top1 - s) > g["GAP"]:
                    break  # sharp drop-off = the rest is noise
                _id, text, role, ts = self.meta[idx]
                out.append({"text": text, "score": round(s, 4),
                            "role": role, "ts": ts, "weak": weak})
            return out


STORE = Store()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/health":
            return self._send(200, {"ok": True, "chunks": len(STORE.meta)})
        if u.path == "/recall":
            qs = parse_qs(u.query)
            query = (qs.get("q") or [""])[0]
            limit = int((qs.get("limit") or ["3"])[0])
            if not query.strip():
                return self._send(400, {"error": "missing q"})
            try:
                return self._send(200, {"results": STORE.recall(query, limit)})
            except Exception as e:
                return self._send(500, {"error": str(e)})
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if urlparse(self.path).path == "/reload":
            STORE.load()
            return self._send(200, {"ok": True, "chunks": len(STORE.meta)})
        self._send(404, {"error": "not found"})

    def log_message(self, *a):
        pass  # quiet


if __name__ == "__main__":
    print(f"conversation-memory API on :{c.API_PORT}  ({len(STORE.meta)} chunks loaded)")
    ThreadingHTTPServer(("127.0.0.1", c.API_PORT), Handler).serve_forever()
