from telebot import types
from db import get_users, add_admin
from config import ADMINS
from subscription import add_channel, remove_channel, get_channels

def is_admin(user_id):
    return user_id in ADMINS

def admin_menu(bot, chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Kanal qo‘shish", "➖ Kanal o‘chirish")
    markup.add("📊 Statistika", "📢 Reklama yuborish")
    bot.send_message(chat_id, "🔧 Admin panel:", reply_markup=markup)

def handle_admin_commands(bot, message):
    if message.text == "➕ Kanal qo‘shish":
        bot.send_message(message.chat.id, "🆔 Kanal username-ni yuboring (@ bilan):")
        bot.register_next_step_handler(message, lambda m: save_channel(bot, m))
    elif message.text == "➖ Kanal o‘chirish":
        bot.send_message(message.chat.id, "🗑 O‘chiriladigan kanalni yuboring:")
        bot.register_next_step_handler(message, lambda m: del_channel(bot, m))
    elif message.text == "📊 Statistika":
        users = len(get_users())
        bot.send_message(message.chat.id, f"👥 Jami foydalanuvchilar: {users}")
    elif message.text == "📢 Reklama yuborish":
        bot.send_message(message.chat.id, "✍️ Reklama matnini yuboring:")
        bot.register_next_step_handler(message, lambda m: send_ad(bot, m))

def save_channel(bot, message):
    if message.text.startswith("@"):
        add_channel(message.text)
        bot.send_message(message.chat.id, f"✅ {message.text} qo‘shildi.")
    else:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri format.")

def del_channel(bot, message):
    remove_channel(message.text)
    bot.send_message(message.chat.id, f"✅ {message.text} o‘chirildi.")

def send_ad(bot, message):
    users = get_users()
    count = 0
    for u in users:
        try:
            bot.send_message(u, message.text)
            count += 1
        except:
            pass
    bot.send_message(message.chat.id, f"✅ {count} foydalanuvchiga yuborildi.")
