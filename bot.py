import telebot
from telebot import types
import requests
import time
from config import BOT_TOKEN, ADMINS
from db import Database
from keep_alive import keep_alive

bot = telebot.TeleBot(BOT_TOKEN)

def check_subscription(user_id):
    channels = Database.get_channels()
    for channel in channels:
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
    Database.add_user(user_id, message.from_user.username)
    channels = Database.get_channels()

    if not channels:
        bot.send_message(message.chat.id, "👋 Salom! Hozircha majburiy obuna kanallari mavjud emas.\nEndi havolani yuboring (YouTube, Instagram yoki TikTok).")
        return

    markup = types.InlineKeyboardMarkup()
    for channel in channels:
        markup.add(types.InlineKeyboardButton(text=f"📢 Kanalga obuna bo‘lish", url=f"https://t.me/{channel.replace('@', '')}"))
    markup.add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data="check_sub"))
    bot.send_message(message.chat.id, "👋 Salom! Videoni yuklab olishdan oldin quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub(call):
    if check_subscription(call.from_user.id):
        bot.send_message(call.message.chat.id, "✅ Tabriklaymiz! Endi video yoki rasm havolasini yuboring (Instagram, YouTube, TikTok).")
    else:
        bot.answer_callback_query(call.id, "❌ Iltimos, barcha kanallarga obuna bo‘ling.", show_alert=True)

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def download_video(message):
    url = message.text.strip()
    bot.send_message(message.chat.id, "⏳ Yuklanmoqda, biroz kuting...")
    try:
        api_url = f"https://api.douyin.wtf/api?url={url}"
        response = requests.get(api_url).json()

        if "video" in response:
            video_url = response["video"]
            caption = response.get("desc", "🎬 Video yuklandi!")
            bot.send_video(message.chat.id, video_url, caption=caption)
        elif "image" in response:
            image_url = response["image"]
            bot.send_photo(message.chat.id, image_url, caption="🖼 Rasm yuklandi!")
        else:
            bot.send_message(message.chat.id, "❌ Videoni yuklab bo‘lmadi, boshqa havola yuboring.")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Xatolik: video yuklab bo‘lmadi.\n{e}")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id in ADMINS:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📢 Reklama yuborish", "📊 Statistika")
        markup.add("➕ Kanal qo‘shish", "➖ Kanal o‘chirish", "👤 Admin qo‘shish")
        bot.send_message(message.chat.id, "🔧 Admin panel:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "❌ Siz admin emassiz.")

@bot.message_handler(func=lambda message: message.text == "📢 Reklama yuborish")
def send_ad(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "✍️ Reklama matnini yuboring.")
        bot.register_next_step_handler(message, process_ad)

def process_ad(message):
    users = Database.get_users()
    count = 0
    for user in users:
        try:
            bot.send_message(user, message.text)
            count += 1
            time.sleep(0.1)
        except:
            pass
    bot.send_message(message.chat.id, f"✅ Reklama {count} foydalanuvchiga yuborildi.")

@bot.message_handler(func=lambda message: message.text == "📊 Statistika")
def stats(message):
    if message.from_user.id in ADMINS:
        total_users = len(Database.get_users())
        total_channels = len(Database.get_channels())
        bot.send_message(message.chat.id, f"👥 Foydalanuvchilar: {total_users}\n📢 Kanallar: {total_channels}")

@bot.message_handler(func=lambda message: message.text == "➕ Kanal qo‘shish")
def add_channel(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "📢 Kanal username ni yuboring (@ bilan).")
        bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    channel = message.text.strip()
    if channel.startswith("@"):
        Database.add_channel(channel)
        bot.send_message(message.chat.id, f"✅ {channel} kanal majburiy obunaga qo‘shildi.")
    else:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri format.")

@bot.message_handler(func=lambda message: message.text == "➖ Kanal o‘chirish")
def remove_channel(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "🗑 O‘chirmoqchi bo‘lgan kanalni yuboring (@ bilan).")
        bot.register_next_step_handler(message, delete_channel)

def delete_channel(message):
    channel = message.text.strip()
    Database.remove_channel(channel)
    bot.send_message(message.chat.id, f"✅ {channel} o‘chirildi.")

@bot.message_handler(func=lambda message: message.text == "👤 Admin qo‘shish")
def add_admin(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "🆔 Yangi admin ID sini yuboring.")
        bot.register_next_step_handler(message, save_admin)

def save_admin(message):
    try:
        admin_id = int(message.text)
        Database.add_admin(admin_id)
        bot.send_message(message.chat.id, f"✅ {admin_id} admin sifatida qo‘shildi.")
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri ID format.")

keep_alive()
bot.polling(non_stop=True)
