import sqlite3
from sqlite3 import Connection
from flask import g

def get_connection() -> Connection:
    conn = sqlite3.connect("database.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def execute(sql: str, params=[]) -> None:
    conn = get_connection()
    result = conn.execute(sql, params)
    conn.commit()
    g.last_insert_id = result.lastrowid
    conn.close()

def query(sql: str, params=[]) -> list:
    conn = get_connection()
    result = conn.execute(sql, params).fetchall()
    conn.close()
    return result

def query_one(sql: str, params=[]) -> list:
    conn = get_connection()
    result = conn.execute(sql, params).fetchone()
    conn.close()
    return result