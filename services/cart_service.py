import json
from db.database import get_db

class CartService:
    def __init__(self):
        self.conn = get_db()

    def get_cart(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute("SELECT items FROM carts WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return []

    def add_to_cart(self, user_id: int, item: dict):
        cart = self.get_cart(user_id)
        cart.append(item)
        self.save_cart(user_id, cart)

    def save_cart(self, user_id: int, items: list):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM carts WHERE user_id = ?", (user_id,))
        cursor.execute("INSERT INTO carts (user_id, items) VALUES (?, ?)", (user_id, json.dumps(items)))
        self.conn.commit()

    def clear_cart(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM carts WHERE user_id = ?", (user_id,))
        self.conn.commit()
