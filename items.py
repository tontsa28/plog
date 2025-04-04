import db

def add_item(user_id: int, manufacturer: str, model: str, registration: str, category: str, airline: str, times_onboard: int = 0, times_seen: int = 0) -> None:
    sql = """INSERT INTO aircraft (manufacturer, model, registration, category, airline, times_onboard, times_seen, user_id)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [manufacturer, model, registration, category, airline, times_onboard, times_seen, user_id])

def remove_item(item_id: int) -> None:
    sql = "DELETE FROM aircraft WHERE id = ?"
    db.execute(sql, [item_id])

def get_items():
    sql = "SELECT * FROM aircraft"
    return db.query(sql)