import sqlite3
from sqlite3 import Connection
from flask import g, flash

def connect() -> Connection:
    conn = sqlite3.connect("database.db")
    conn.cursor().execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row

    return conn

def execute(sql: str, params: list | None = None) -> None:
    conn = connect()
    if params is None:
        params = []

    result = conn.cursor().execute(sql, params)
    conn.commit()

    g.last_insert_id = result.lastrowid
    conn.close()

def execute_transaction(sqls: list[str], all_params: list[list] | None = None) -> None:
    conn = connect()
    if all_params is None:
        all_params = [[] for _ in range(len(sqls))]
    
    try:
        conn.cursor().execute("BEGIN")

        for sql, params in zip(sqls, all_params):
            conn.cursor().execute(sql, params)

        conn.commit()
        g.last_insert_id = conn.cursor().lastrowid
    except sqlite3.Error:
        conn.rollback()
        flash("ERROR: database transaction execution failed, no changes were made")
    finally:
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

    return dict(result) if result else dict()