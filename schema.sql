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
    location TEXT,
    airport TEXT,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    aircraft_id INTEGER REFERENCES aircraft(id) UNIQUE,
    image BLOB
);

CREATE TABLE manufacturers (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE likes (
    id INTEGER PRIMARY KEY,
    aircraft_id INTEGER REFERENCES aircraft(id),
    user_id INTEGER REFERENCES users(id)
);