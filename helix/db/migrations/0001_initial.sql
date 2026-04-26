CREATE TABLE IF NOT EXISTS files (
    id              TEXT PRIMARY KEY,
    file_path       TEXT NOT NULL UNIQUE,
    file_hash       TEXT NOT NULL,
    file_name       TEXT NOT NULL,
    extension       TEXT NOT NULL,
    mime_type       TEXT NOT NULL,
    file_size_kb    REAL NOT NULL,
    created_at      TEXT,
    modified_at     TEXT,
    indexed_at      TEXT NOT NULL,
    category        TEXT,
    tags            TEXT,
    summary         TEXT,
    raw_text        TEXT,
    full_text_path  TEXT,
    confidence      REAL,
    model_used      TEXT,
    processor_ver   TEXT,
    status          TEXT NOT NULL DEFAULT 'pending',
    error_msg       TEXT
);

CREATE INDEX IF NOT EXISTS idx_files_status ON files(status);
CREATE INDEX IF NOT EXISTS idx_files_hash ON files(file_hash);
CREATE INDEX IF NOT EXISTS idx_files_category ON files(category);
CREATE INDEX IF NOT EXISTS idx_files_indexed_at ON files(indexed_at);

CREATE TABLE IF NOT EXISTS chunks (
    id              TEXT PRIMARY KEY,
    file_id         TEXT NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    chunk_index     INTEGER NOT NULL,
    text            TEXT NOT NULL,
    chroma_doc_id   TEXT NOT NULL UNIQUE,
    token_count     INTEGER,
    created_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_chunks_file_id ON chunks(file_id);

CREATE TABLE IF NOT EXISTS tasks (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    description     TEXT,
    source_file_id  TEXT REFERENCES files(id),
    source_text     TEXT,
    deadline        TEXT,
    priority        TEXT NOT NULL DEFAULT 'medium',
    status          TEXT NOT NULL DEFAULT 'todo',
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    completed_at    TEXT,
    recurrence      TEXT,
    tags            TEXT
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_deadline ON tasks(deadline);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);

CREATE TABLE IF NOT EXISTS reminders (
    id              TEXT PRIMARY KEY,
    task_id         TEXT REFERENCES tasks(id) ON DELETE CASCADE,
    message         TEXT NOT NULL,
    remind_at       TEXT NOT NULL,
    delivered       INTEGER NOT NULL DEFAULT 0,
    snoozed_until   TEXT,
    created_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_reminders_remind_at ON reminders(remind_at);
CREATE INDEX IF NOT EXISTS idx_reminders_delivered ON reminders(delivered);

CREATE TABLE IF NOT EXISTS calendar_events (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    description     TEXT,
    start_dt        TEXT NOT NULL,
    end_dt          TEXT,
    all_day         INTEGER NOT NULL DEFAULT 0,
    location        TEXT,
    source_file_id  TEXT REFERENCES files(id),
    category        TEXT,
    ical_uid        TEXT UNIQUE,
    created_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_start_dt ON calendar_events(start_dt);

CREATE TABLE IF NOT EXISTS conversations (
    id              TEXT PRIMARY KEY,
    session_id      TEXT NOT NULL,
    turn_index      INTEGER NOT NULL,
    role            TEXT NOT NULL,
    content         TEXT NOT NULL,
    timestamp       TEXT NOT NULL,
    memory_tier     TEXT NOT NULL DEFAULT 'working',
    token_count     INTEGER,
    model_used      TEXT
);

CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conv_timestamp ON conversations(timestamp);
CREATE INDEX IF NOT EXISTS idx_conv_tier ON conversations(memory_tier);

CREATE TABLE IF NOT EXISTS memory_facts (
    id              TEXT PRIMARY KEY,
    fact            TEXT NOT NULL,
    confidence      REAL NOT NULL DEFAULT 0.8,
    source_session  TEXT,
    created_at      TEXT NOT NULL,
    last_accessed   TEXT NOT NULL,
    access_count    INTEGER NOT NULL DEFAULT 0,
    is_preference   INTEGER NOT NULL DEFAULT 0,
    is_rule         INTEGER NOT NULL DEFAULT 0,
    superseded_by   TEXT REFERENCES memory_facts(id)
);

CREATE TABLE IF NOT EXISTS graph_nodes (
    id              TEXT PRIMARY KEY,
    label           TEXT NOT NULL,
    node_type       TEXT NOT NULL,
    file_id         TEXT REFERENCES files(id),
    properties      TEXT,
    created_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS graph_edges (
    id              TEXT PRIMARY KEY,
    source_id       TEXT NOT NULL REFERENCES graph_nodes(id) ON DELETE CASCADE,
    target_id       TEXT NOT NULL REFERENCES graph_nodes(id) ON DELETE CASCADE,
    relation        TEXT NOT NULL,
    weight          REAL NOT NULL DEFAULT 1.0,
    created_at      TEXT NOT NULL,
    UNIQUE(source_id, target_id, relation)
);

CREATE INDEX IF NOT EXISTS idx_edges_source ON graph_edges(source_id);
CREATE INDEX IF NOT EXISTS idx_edges_target ON graph_edges(target_id);

CREATE TABLE IF NOT EXISTS reflex_rules (
    id              TEXT PRIMARY KEY,
    rule_text       TEXT NOT NULL,
    rule_type       TEXT NOT NULL DEFAULT 'behavioural',
    confidence      REAL NOT NULL DEFAULT 0.7,
    created_at      TEXT NOT NULL,
    last_triggered  TEXT,
    triggered_count INTEGER NOT NULL DEFAULT 0,
    archived        INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS schema_migrations (
    version         INTEGER PRIMARY KEY,
    name            TEXT NOT NULL,
    applied_at      TEXT NOT NULL
);
