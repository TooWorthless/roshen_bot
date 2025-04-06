import json
import telebot
from telebot import types
from config import TOKEN, PRODUCTS_PATH
from services.cart_service import CartService
from services.order_service import OrderService

bot = telebot.TeleBot(TOKEN)
cart_service = CartService()
order_service = OrderService()

with open(PRODUCTS_PATH, 'r', encoding='utf-8') as f:
    products_data = json.load(f)

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('📦 Каталог', '🛒 Моє замовлення')
    bot.send_message(message.chat.id, f"Привіт, {message.from_user.first_name}! 👋\nОберіть дію:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == '📦 Каталог')
def show_categories(message):
    markup = types.InlineKeyboardMarkup()
    for category in products_data:
        markup.add(types.InlineKeyboardButton(text=category, callback_data=f"category:{category}"))
    bot.send_message(message.chat.id, "Оберіть категорію продукції:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('category:'))
def show_products(call):
    category = call.data.split(':')[1]
    markup = types.InlineKeyboardMarkup()
    for product in products_data[category]:
        callback_data = f"add:{product['name']}:{product['price']}"
        markup.add(types.InlineKeyboardButton(text=f"{product['name']} - {product['price']} грн", callback_data=callback_data))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"Категорія: {category}\nОберіть товар:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('add:'))
def add_to_cart(call):
    _, name, price = call.data.split(':')
    cart_service.add_to_cart(call.from_user.id, {"name": name, "price": int(price)})
    bot.answer_callback_query(call.id, f"✅ Додано: {name}")

@bot.message_handler(func=lambda msg: msg.text == '🛒 Моє замовлення')
def show_cart(message):
    cart = cart_service.get_cart(message.from_user.id)
    if not cart:
        bot.send_message(message.chat.id, "🛒 Ваш кошик порожній.")
        return

    text = "🧺 Ваше замовлення:\n"
    total = 0
    for item in cart:
        text += f"- {item['name']}: {item['price']} грн\n"
        total += item['price']
    text += f"\n💰 Разом: {total} грн"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Підтвердити", callback_data="confirm"),
               types.InlineKeyboardButton("❌ Очистити", callback_data="clear"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['confirm', 'clear'])
def handle_cart_action(call):
    user_id = call.from_user.id
    if call.data == 'clear':
        cart_service.clear_cart(user_id)
        bot.answer_callback_query(call.id, "🧹 Кошик очищено.")
        bot.edit_message_text("Кошик очищено.", call.message.chat.id, call.message.message_id)
    elif call.data == 'confirm':
        cart = cart_service.get_cart(user_id)
        if not cart:
            bot.answer_callback_query(call.id, "Кошик порожній.")
            return
        order_service.create_order(user_id, call.from_user.username or '', cart)
        cart_service.clear_cart(user_id)
        bot.answer_callback_query(call.id, "🧾 Замовлення оформлено!")
        bot.edit_message_text("Дякуємо! Ваше замовлення збережено 🧁", call.message.chat.id, call.message.message_id)
