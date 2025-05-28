-- database: timelines.db

-- Build system tables only if they don't already exist
CREATE TABLE IF NOT EXISTS events(
    event_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    event_name TEXT
);

CREATE TABLE IF NOT EXISTS rooms(
    room_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    room_name TEXT
);

CREATE TABLE IF NOT EXISTS guides(
    guide_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    guide_name TEXT
);

CREATE TABLE IF NOT EXISTS event_rooms (
    event_id INT,
    room_id INT,
    PRIMARY KEY (event_id, room_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

CREATE TABLE IF NOT EXISTS event_guides(
    event_id INT,
    guide_id INT,
    PRIMARY KEY (event_id, guide_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (guide_id) REFERENCES guides(guide_id)
);

CREATE TABLE IF NOT EXISTS guide_occupation(
    id PRIMARY KEY AUTOINCREMENT NOT NULL,
    guide_id INT,
    available_from DATETIME,
    available_to DATETIME,
    FOREIGN KEY (guide_id) REFERENCES guides(guide_id),
    reason TEXT
);

CREATE TABLE IF NOT EXISTS room_occupation(
    id PRIMARY KEY AUTOINCREMENT NOT NULL,
    room_id INT,
    busy_from DATETIME,
    busy_to DATETIME,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
    reason TEXT
);
