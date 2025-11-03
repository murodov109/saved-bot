import telebot
from telebot import types
import requests
import re
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
        except:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    add_user(user_id, message.from_user.username)
    channels = get_channels()
    if channels:
        markup = types.InlineKeyboardMarkup()
        for channel in channels:
            markup.add(types.InlineKeyboardButton(f"📢 {channel}", url=f"https://t.me/{channel.replace('@','')}"))
        markup.add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data="check_sub"))
        bot.send_message(message.chat.id, "👇 Quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "🎬 Havolani yuboring (Instagram, TikTok, YouTube).")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub(call):
    if check_subscription(call.from_user.id):
        bot.send_message(call.message.chat.id, "✅ Tabriklaymiz! Endi video yoki rasm havolasini yuboring.")
    else:
        bot.answer_callback_query(call.id, "❌ Hali barcha kanallarga obuna bo‘lmadingiz.", show_alert=True)

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id in ADMINS or message.from_user.id in get_admins():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("➕ Kanal qo‘shish", "➖ Kanal o‘chirish", "📢 Reklama yuborish", "👤 Admin qo‘shish", "📊 Statistika")
        bot.send_message(message.chat.id, "🔧 Admin panel:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "❌ Siz admin emassiz.")

@bot.message_handler(func=lambda m: m.text == "📊 Statistika")
def stats(message):
    total = len(get_users())
    bot.send_message(message.chat.id, f"👥 Jami foydalanuvchilar: {total}")

@bot.message_handler(func=lambda m: m.text == "📢 Reklama yuborish")
def ad_send(message):
    bot.send_message(message.chat.id, "✍️ Reklama matnini yuboring:")
    bot.register_next_step_handler(message, send_ad)

def send_ad(message):
    users = get_users()
    count = 0
    for user in users:
        try:
            bot.send_message(user, message.text)
            count += 1
        except:
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
    except:
        bot.send_message(message.chat.id, "❌ Xatolik.")

def get_video_url(url):
    if "instagram" in url:
        api = f"https://snapinsta.app/api?url={url}"
    elif "tiktok" in url:
        api = f"https://www.tikwm.com/api/?url={url}"
    elif "youtube" in url:
        api = f"https://api.zenoapi.com/youtube?url={url}"
    else:
        return None
    try:
        r = requests.get(api, timeout=10)
        data = r.json()
        if "video" in data:
            return data["video"]
        elif "url" in data:
            return data["url"]
        elif "data" in data and "play" in data["data"]:
            return data["data"]["play"]
    except:
        return None

@bot.message_handler(func=lambda message: re.match(r'https?://', message.text))
def downloader(message):
    url = message.text.strip()
    bot.send_message(message.chat.id, "⏳ Yuklanmoqda...")
    video = get_video_url(url)
    if video:
        try:
            bot.send_video(message.chat.id, video, caption="🎬 Yuklab olindi!")
        except:
            bot.send_message(message.chat.id, f"🔗 Yuklab olish uchun: {video}")
    else:
        bot.send_message(message.chat.id, "❌ Videoni yuklab bo‘lmadi.")

keep_alive()
bot.polling(non_stop=True)
