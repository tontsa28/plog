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
    aircraft_id INTEGER REFERENCES UNIQUE aircraft,
    image BLOB
);

CREATE TABLE manufacturers (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE aircraft_manufacturers (
    id INTEGER PRIMARY KEY,
    aircraft_id INTEGER REFERENCES aircraft,
    manufacturer_id INTEGER REFERENCES manufacturers
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE aircraft_categories (
    id INTEGER PRIMARY KEY,
    aircraft_id INTEGER REFERENCES aircraft,
    manufacturer_id INTEGER REFERENCES categories
);

CREATE TABLE likes (
    id INTEGER PRIMARY KEY,
    aircraft_id INTEGER REFERENCES aircraft,
    user_id INTEGER REFERENCES users
);