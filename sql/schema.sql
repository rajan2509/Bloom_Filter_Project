
-- Bloom Filter Project Database

CREATE TABLE IF NOT EXISTS checked_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    item_type TEXT NOT NULL
        CHECK (item_type IN ('username', 'url')),

    item_value TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (item_type, item_value)
);

-- Index for faster database searches
CREATE INDEX IF NOT EXISTS idx_item_lookup
ON checked_items(item_type, item_value);
