from werkzeug.security import check_password_hash, generate_password_hash

import db

def get_user(user_id: int) -> list:
    sql = "SELECT id, username FROM users WHERE id = ?"
    return db.query_one(sql, [user_id])

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