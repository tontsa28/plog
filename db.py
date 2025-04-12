import sqlite3
from sqlite3 import Connection
from flask import g

def connect() -> Connection:
    conn = sqlite3.connect("database.db")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row

    return conn

def execute(sql: str, params: list | None = None) -> None:
    conn = connect()
    if params is None:
        params = []

    result = conn.execute(sql, params)
    conn.commit()

    g.last_insert_id = result.lastrowid
    conn.close()

def query(sql: str, params: list | None = None) -> list[dict]:
    conn = connect()
    if params is None:
        params = []

    result = conn.cursor().execute(sql, params).fetchall()
    conn.close()

    return [dict(res) for res in result]

def query_one(sql: str, params: list | None = None) -> dict:
    conn = connect()
    if params is None:
        params = []

    result = conn.cursor().execute(sql, params).fetchone()
    conn.close()

    return dict(result)