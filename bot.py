import telebot
from telebot import types
from config import BOT_TOKEN, ADMINS, MANDATORY_CHANNELS
from db import add_user, add_admin, get_admins
import requests

bot = telebot.TeleBot(BOT_TOKEN)

def check_subscription(user_id):
    for channel in MANDATORY_CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id)
            if status.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user.id, message.from_user.username)
    markup = types.InlineKeyboardMarkup()
    for ch in MANDATORY_CHANNELS:
        markup.add(types.InlineKeyboardButton(f"➕ {ch} kanaliga obuna bo‘lish", url=f"https://t.me/{ch.replace('@','')}"))
    markup.add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data="verify"))
    bot.send_message(message.chat.id, "📢 Quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify_subscription(call):
    if check_subscription(call.from_user.id):
        bot.send_message(call.message.chat.id, "✅ Obuna tasdiqlandi! Endi video yoki rasm havolasini yuboring.")
    else:
        bot.send_message(call.message.chat.id, "❌ Siz hali barcha kanallarga obuna bo‘lmagansiz!")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id in get_admins() or message.from_user.id in ADMINS:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Reklama tarqatish", callback_data="broadcast"))
        markup.add(types.InlineKeyboardButton("➕ Yangi admin qo‘shish", callback_data="add_admin"))
        markup.add(types.InlineKeyboardButton("📊 Statistika", callback_data="stats"))
        bot.send_message(message.chat.id, "🛠 Admin panel:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "❌ Siz admin emassiz.")

@bot.callback_query_handler(func=lambda call: call.data == "add_admin")
def add_admin_handler(call):
    if call.from_user.id in get_admins() or call.from_user.id in ADMINS:
        bot.send_message(call.message.chat.id, "Yangi admin ID raqamini yuboring:")
        bot.register_next_step_handler(call.message, process_new_admin)

def process_new_admin(message):
    try:
        new_admin_id = int(message.text)
        add_admin(new_admin_id)
        bot.send_message(message.chat.id, "✅ Yangi admin muvaffaqiyatli qo‘shildi!")
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri ID kiritildi!")

@bot.callback_query_handler(func=lambda call: call.data == "broadcast")
def broadcast_message(call):
    if call.from_user.id in get_admins() or call.from_user.id in ADMINS:
        bot.send_message(call.message.chat.id, "Reklama matnini yuboring:")
        bot.register_next_step_handler(call.message, send_broadcast)

def send_broadcast(message):
    conn = sqlite3.connect("database.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    users = [row[0] for row in cur.fetchall()]
    conn.close()
    count = 0
    for user in users:
        try:
            bot.send_message(user, message.text)
            count += 1
        except:
            continue
    bot.send_message(message.chat.id, f"📨 {count} ta foydalanuvchiga yuborildi.")

@bot.callback_query_handler(func=lambda call: call.data == "stats")
def show_stats(call):
    conn = sqlite3.connect("database.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]
    conn.close()
    bot.send_message(call.message.chat.id, f"📊 Jami foydalanuvchilar: {total_users}")

@bot.message_handler(content_types=['text'])
def download_video(message):
    if check_subscription(message.from_user.id):
        url = message.text
        if "http" not in url:
            bot.send_message(message.chat.id, "❌ Iltimos, to‘g‘ri video havolasini yuboring.")
            return
        bot.send_message(message.chat.id, "⏳ Yuklanmoqda, biroz kuting...")
        try:
            # Faqat demo uchun, real yuklab olish uchun API kerak bo‘ladi
            bot.send_message(message.chat.id, f"✅ Yuklab olish tayyor:\n{url}")
        except:
            bot.send_message(message.chat.id, "❌ Yuklab olishda xatolik yuz berdi.")
    else:
        bot.send_message(message.chat.id, "⚠️ Avval kanallarga obuna bo‘ling va tasdiqlang!")

bot.polling(none_stop=True)
