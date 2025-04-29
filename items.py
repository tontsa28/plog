import db

def add_item(
    user_id: int,
    manufacturer: str,
    model: str,
    registration: str,
    category: str,
    airline: str,
    times_onboard: int = 0,
    times_seen: int = 0
) -> None:
    sql = """INSERT INTO aircraft (manufacturer, model, registration, category, airline, times_onboard, times_seen, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [manufacturer, model, registration, category, airline, times_onboard, times_seen, user_id])

def remove_item(item_id: int) -> None:
    sql1 = "DELETE FROM likes WHERE aircraft_id = ?"
    sql2 = "DELETE FROM aircraft WHERE id = ?"
    db.execute_transaction([sql1, sql2], [[item_id], [item_id]])

def get_items() -> list:
    sql = """SELECT A.id,
                    A.manufacturer,
                    A.model,
                    A.registration,
                    A.airline,
                    A.user_id,
                    U.username
            FROM aircraft A, users U
            WHERE A.user_id = U.id"""
    return db.query(sql)

def get_item(item_id: int) -> dict:
    sql = """SELECT A.id,
                    A.manufacturer,
                    A.model,
                    A.registration,
                    A.category,
                    A.airline,
                    A.times_onboard,
                    A.times_seen,
                    A.user_id,
                    U.username
            FROM aircraft A, users U
            WHERE A.user_id = U.id AND A.id = ?"""
    return db.query_one(sql, [item_id])

def update_item(
    item_id: int,
    manufacturer: str,
    model: str,
    registration: str,
    category: str,
    airline: str,
    times_onboard: int,
    times_seen: int
) -> None:
    sql = """UPDATE aircraft
            SET manufacturer = ?,
                model = ?,
                registration = ?,
                category = ?,
                airline = ?,
                times_onboard = ?,
                times_seen = ?
            WHERE id = ?"""
    db.execute(sql, [manufacturer, model, registration, category, airline, times_onboard, times_seen, item_id])

def get_manufacturers_all() -> list[dict]:
    sql = "SELECT name FROM manufacturers"
    return db.query(sql)

def get_categories_all() -> list[dict]:
    sql = "SELECT name FROM categories"
    return db.query(sql)

def search_items(query: str) -> list[dict]:
    sql = """SELECT A.id,
                    A.manufacturer,
                    A.model,
                    A.registration,
                    A.airline,
                    A.user_id,
                    U.username
            FROM aircraft A, users U
            WHERE A.user_id = U.id
            AND (A.airline || ' ' || A.manufacturer || ' ' || A.model || ' ' || A.registration) LIKE ?"""
    like = "%" + query + "%"

    return db.query(sql, [like])

def add_like(item_id: int, user_id: int) -> None:
    sql = "INSERT INTO likes (aircraft_id, user_id) VALUES (?, ?)"
    db.execute(sql, [item_id, user_id])

def remove_like(item_id: int, user_id: int) -> None:
    sql = "DELETE FROM likes WHERE aircraft_id = ? AND user_id = ?"
    db.execute(sql, [item_id, user_id])

def has_liked(item_id: int, user_id: int) -> bool:
    sql = "SELECT aircraft_id, user_id FROM likes WHERE aircraft_id = ? AND user_id = ?"
    result = db.query_one(sql, [item_id, user_id])

    return True if result else False

def has_liked_all(user_id: int) -> dict:
    sql = "SELECT aircraft_id FROM likes WHERE user_id = ?"

    result = {}
    for aircraft in db.query(sql, [user_id]):
        result[aircraft["aircraft_id"]] = True
    return result

def get_likes(item_id: int) -> dict:
    sql = "SELECT COUNT(*) AS count FROM likes WHERE aircraft_id = ?"

    result = {}
    result[item_id] = db.query_one(sql, [item_id])["count"]
    return result

def get_likes_all() -> dict:
    sql = "SELECT aircraft_id, COUNT(*) AS count FROM likes GROUP BY aircraft_id"

    result = {}
    for aircraft in db.query(sql):
        result[aircraft["aircraft_id"]] = aircraft["count"]
    return result