-- Conversation-memory store. One row per conversation chunk + its embedding.
-- Embeddings are stored as raw float32 bytes (compact, fast to load into numpy).

-- WAL lets the reader (API) and writer (indexer) work concurrently without
-- "database is locked". It's a persistent property of the file, set once.
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS chunks (
    id          INTEGER PRIMARY KEY,
    source      TEXT NOT NULL,          -- where it came from (e.g. 'claude-code')
    session_id  TEXT,
    seq         INTEGER,                -- position within the session
    role        TEXT,                   -- 'user' | 'assistant'
    text        TEXT NOT NULL,
    ts          TEXT,                   -- ISO timestamp of the turn
    cwd         TEXT,                   -- working dir, handy context
    status      TEXT DEFAULT 'active',  -- 'active' | 'noise'  (soft-hide, never delete)
    embedding   BLOB NOT NULL,          -- float32 vector
    UNIQUE(source, session_id, seq)
);

-- Incremental indexing marker per source file (value = file mtime we last indexed).
CREATE TABLE IF NOT EXISTS index_state (
    source_key  TEXT PRIMARY KEY,
    marker      REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_chunks_status ON chunks(status);
