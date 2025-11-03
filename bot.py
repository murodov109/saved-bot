import telebot
from telebot import types
import requests
from config import BOT_TOKEN, ADMINS
from db import add_user, get_users, get_admins, add_admin, add_channel, remove_channel, get_channels
from keep_alive import keep_alive

bot = telebot.TeleBot(BOT_TOKEN)

def check_subscription(user_id):
    for channel in get_channels():
        try:
            status = bot.get_chat_member(channel, user_id)
            if status.status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    add_user(user_id, username)
    channels = get_channels()
    if channels:
        markup = types.InlineKeyboardMarkup()
        for channel in channels:
            markup.add(types.InlineKeyboardButton(f"📢 {channel}", url=f"https://t.me/{channel.replace('@', '')}"))
        markup.add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data="check_sub"))
        bot.send_message(message.chat.id, "👇 Quyidagi kanallarga obuna bo‘ling va tasdiqlang:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "🎬 Havolani yuboring (Instagram, TikTok, YouTube).")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub(call):
    if check_subscription(call.from_user.id):
        bot.send_message(call.message.chat.id, "✅ Obuna tasdiqlandi! Endi video yoki rasm havolasini yuboring.")
    else:
        bot.answer_callback_query(call.id, "❌ Hali barcha kanallarga obuna bo‘lmadingiz.", show_alert=True)

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id in ADMINS or message.from_user.id in get_admins():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("➕ Kanal qo‘shish", "➖ Kanal o‘chirish")
        markup.add("📢 Reklama yuborish", "👤 Admin qo‘shish", "📊 Statistika")
        bot.send_message(message.chat.id, "🔧 Admin panel:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "❌ Siz admin emassiz.")

@bot.message_handler(func=lambda m: m.text == "📊 Statistika")
def stats(message):
    if message.from_user.id in ADMINS or message.from_user.id in get_admins():
        total = len(get_users())
        bot.send_message(message.chat.id, f"👥 Jami foydalanuvchilar: {total}")

@bot.message_handler(func=lambda m: m.text == "📢 Reklama yuborish")
def ad_send(message):
    if message.from_user.id in ADMINS or message.from_user.id in get_admins():
        bot.send_message(message.chat.id, "✍️ Reklama matnini yuboring:")
        bot.register_next_step_handler(message, send_ad)

def send_ad(message):
    users = get_users()
    count = 0
    for user in users:
        try:
            bot.send_message(user, message.text)
            count += 1
        except Exception:
            pass
    bot.send_message(message.chat.id, f"✅ {count} foydalanuvchiga yuborildi.")

@bot.message_handler(func=lambda m: m.text == "➕ Kanal qo‘shish")
def add_channel_msg(message):
    bot.send_message(message.chat.id, "🆔 Kanal username-ni yuboring (@ bilan):")
    bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    if message.text.startswith("@"):
        add_channel(message.text)
        bot.send_message(message.chat.id, f"✅ {message.text} qo‘shildi.")
    else:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri format.")

@bot.message_handler(func=lambda m: m.text == "➖ Kanal o‘chirish")
def del_channel(message):
    bot.send_message(message.chat.id, "🗑 O‘chiriladigan kanalni yuboring:")
    bot.register_next_step_handler(message, delete_channel)

def delete_channel(message):
    remove_channel(message.text)
    bot.send_message(message.chat.id, f"✅ {message.text} o‘chirildi.")

@bot.message_handler(func=lambda m: m.text == "👤 Admin qo‘shish")
def add_admin_msg(message):
    bot.send_message(message.chat.id, "🆔 Yangi admin ID sini yuboring:")
    bot.register_next_step_handler(message, save_admin)

def save_admin(message):
    try:
        add_admin(int(message.text))
        bot.send_message(message.chat.id, f"✅ Admin {message.text} qo‘shildi.")
    except Exception:
        bot.send_message(message.chat.id, "❌ Xatolik yuz berdi.")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def download_video(message):
    bot.send_message(message.chat.id, "⏳ Yuklanmoqda, biroz kuting...")
    try:
        url = f"https://api.douyin.wtf/api?url={message.text}"
        res = requests.get(url).json()
        if "video" in res:
            bot.send_video(message.chat.id, res["video"], caption="🎬 Video yuklandi!")
        elif "image" in res:
            bot.send_photo(message.chat.id, res["image"], caption="🖼 Rasm yuklandi!")
        else:
            bot.send_message(message.chat.id, "❌ Yuklab bo‘lmadi.")
    except Exception:
        bot.send_message(message.chat.id, "⚠️ Xatolik, boshqa havola yuboring.")

keep_alive()
bot.polling(non_stop=True)
