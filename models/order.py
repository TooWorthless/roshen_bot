from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class OrderItem:
    name: str
    price: int

@dataclass
class Order:
    user_id: int
    username: str
    items: List[OrderItem]
    created_at: str = datetime.now().isoformat()
    status: str = 'Новий'
