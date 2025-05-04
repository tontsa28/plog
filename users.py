from werkzeug.security import check_password_hash, generate_password_hash

import db

def get_user(user_id: int) -> dict:
    sql = "SELECT id, username FROM users WHERE id = ?"
    return db.query_one(sql, [user_id])

def get_items(user_id: int) -> list[dict]:
    sql = """SELECT id,
                    manufacturer,
                    model,
                    registration,
                    airline
            FROM aircraft
            WHERE user_id = ?"""
    return db.query(sql, [user_id])

def get_likes_all(user_id: int) -> dict:
    sql = """SELECT aircraft_id,
                    COUNT(*) AS count
            FROM likes
            WHERE user_id = ?
            GROUP BY aircraft_id"""

    result = {}
    for aircraft in db.query(sql, [user_id]):
        result[aircraft["aircraft_id"]] = aircraft["count"]
    return result

def has_images(user_id: int) -> dict:
    sql = """SELECT I.aircraft_id
            FROM images I, aircraft A
            WHERE I.aircraft_id = A.id
            AND A.user_id = ?"""

    result = {}
    for aircraft in db.query(sql, [user_id]):
        result[aircraft["aircraft_id"]] = True
    return result

def register_user(username: str, password: str) -> None:
    password = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (?, ?)"
    db.execute(sql, [username, password])

def check_login(username: str, password: str) -> str | None:
    sql = "SELECT id, password FROM users WHERE username = ?"
    result = db.query_one(sql, [username])
    if not result:
        return None

    user_id = result["id"]
    password_hash = result["password"]
    if check_password_hash(password_hash, password):
        return user_id
    return None