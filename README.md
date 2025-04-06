
# 🤖 RoshenBot

**RoshenBot** — це Telegram-бот для оформлення замовлень продукції Roshen. Користувачі можуть обрати товари, додати їх у кошик та оформити замовлення.

## ⚙️ Можливості
- Перегляд категорій товарів (шоколад, цукерки, торти тощо)
- Додавання товарів у кошик
- Збереження кошика в SQLite
- Оформлення замовлення з підтвердженням

## 📦 Структура
```
roshen_bot/
├── bot.py
├── config.py
├── data/products.json
├── db/
│   ├── database.py
│   └── database.db
├── handlers/main.py
├── models/order.py
├── services/
│   ├── cart_service.py
│   └── order_service.py
```

## ▶️ Запуск
1. Встановити залежності: `pip install -r requirements.txt`
2. Вставити ваш токен у `config.py`, перед цим замінити `config.example.py` на `config.py`
3. Запустити бота: `python bot.py`
