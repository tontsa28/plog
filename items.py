import db

def add_item(user_id: int, manufacturer: str, model: str, registration: str, category: str, airline: str, times_onboard: int = 0, times_seen: int = 0) -> None:
    sql = """INSERT INTO aircraft (manufacturer, model, registration, category, airline, times_onboard, times_seen, user_id)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [manufacturer, model, registration, category, airline, times_onboard, times_seen, user_id])

def remove_item(item_id: int) -> None:
    sql = "DELETE FROM aircraft WHERE id = ?"
    db.execute(sql, [item_id])

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

def get_item(item_id: int) -> list | None:
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

def update_item(item_id: int, manufacturer: str, model: str, registration: str, category: str, airline: str, times_onboard: int, times_seen: int) -> None:
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