CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE aircraft (
    id INTEGER PRIMARY KEY,
    manufacturer TEXT,
    model TEXT,
    registration TEXT,
    category TEXT,
    airline TEXT,
    times_onboard INTEGER,
    times_seen INTEGER,
    user_id INTEGER REFERENCES users
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    aircraft_id INTEGER REFERENCES aircraft,
    image BLOB
);