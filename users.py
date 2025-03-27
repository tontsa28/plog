from werkzeug.security import check_password_hash, generate_password_hash

import db

def get_user(user_id: int):
    sql = "SELECT id, username FROM users WHERE id = ?;"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_items(user_id):
    sql = "SELECT id, title FROM items WHERE user_id = ? ORDER BY id DESC;"
    return db.query(sql, [user_id])

def register_user(username, password):
    password = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (?, ?);"
    db.execute(sql, [username, password])

def check_login(username, password):
    sql = "SELECT id, password FROM users WHERE username = ?;"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None