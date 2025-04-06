import json
from datetime import datetime
from db.database import get_db

class OrderService:
    def __init__(self):
        self.conn = get_db()

    def create_order(self, user_id, username, items):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO orders (user_id, username, items, created_at)
            VALUES (?, ?, ?, ?)
        ''', (
            user_id,
            username,
            json.dumps(items, ensure_ascii=False),
            datetime.now().isoformat()
        ))
        self.conn.commit()
