-- Build system tables only if they don't already exist

CREATE TABLE IF NOT EXISTS logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    write_time TEXT DEFAULT (datetime('now', 'localtime')),
    user_id INTEGER,
    user_ip TEXT,
    message TEXT,
);
