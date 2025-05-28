-- database: internal_data.db

-- Build system tables only if they don't already exist
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_name TEXT,
    user_auth TEXT,
    user_pass TEXT
);

CREATE TABLE IF NOT EXISTS logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    write_time TEXT DEFAULT (datetime('now', 'localtime')),
    user_id INTEGER,
    user_ip TEXT,
    message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);