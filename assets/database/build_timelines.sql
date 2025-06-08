-- Build system tables only if they don't already exist
CREATE TABLE IF NOT EXISTS events(
    event_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    event_name TEXT,
    duration INTEGER
);

CREATE TABLE IF NOT EXISTS rooms(
    room_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    room_name TEXT,
    capacity INTEGER
);

CREATE TABLE IF NOT EXISTS guides(
    guide_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS room_event_relation (
    event_id INT,
    room_id INT,
    PRIMARY KEY (event_id, room_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

CREATE TABLE IF NOT EXISTS event_guide_relation (
    event_id INT,
    guide_id INT,
    PRIMARY KEY (event_id, guide_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (guide_id) REFERENCES guides(guide_id)
);

CREATE TABLE IF NOT EXISTS available_events (
    available_event_id INTEGER PRIMARY KEY AUTOINCREMENT NOT null,
    event_id INT,
    room_id INT,
    guide_id INT,
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    FOREIGN KEY (guide_id) REFERENCES guides(guide_id)
);


CREATE TABLE IF NOT EXISTS occupied_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    available_event_id INT,
    guide_oc_id INT,
    room_oc_id INT,
    busy_from INTEGER,
    busy_to INTEGER,
    comment TEXT,
    FOREIGN KEY (available_event_id) REFERENCES available_events(available_event_id),
    FOREIGN KEY (guide_oc_id) REFERENCES guide_occupation(id),
    FOREIGN KEY (room_oc_id) REFERENCES room_occupation(id)
);

CREATE TABLE IF NOT EXISTS guide_occupation(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    guide_id INT,
    busy_from INTEGER,
    busy_to INTEGER,
    reason TEXT,
    FOREIGN KEY (guide_id) REFERENCES guides(guide_id)
);

CREATE TABLE IF NOT EXISTS room_occupation(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    room_id INT,
    busy_from INTEGER,
    busy_to INTEGER,
    reason TEXT,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_name TEXT,
    user_mail TEXT,
    user_auth TEXT,
    user_pass_hash TEXT,
    user_salt TEXT,
    cookie TEXT
);

CREATE TABLE IF NOT EXISTS admins(
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS mods(
    mod_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS work_hours(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    guide_id INT,
    week_day INT,
    start_hour TEXT,
    end_hour TEXT
)