import telebot
from telebot import types
import requests
from keep_alive import keep_alive
from db import add_user, get_admins, add_admin, get_channels, add_channel, remove_channel
from config import BOT_TOKEN, ADMINS

bot = telebot.TeleBot(BOT_TOKEN)
keep_alive()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    add_user(user_id)
    channels = get_channels()
    if not channels:
        bot.send_message(user_id, "Majburiy obuna uchun kanallar hozircha yo‘q. /admin orqali sozlang.")
        return
    markup = types.InlineKeyboardMarkup()
    for ch in channels:
        markup.add(types.InlineKeyboardButton("🔗 Kanalga o‘tish", url=f"https://t.me/{ch.replace('@','')}"))
    markup.add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data="check_subs"))
    bot.send_message(user_id, "Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subs(call):
    user_id = call.from_user.id
    channels = get_channels()
    not_subscribed = []
    for ch in channels:
        try:
            status = bot.get_chat_member(ch, user_id)
            if status.status not in ["member", "administrator", "creator"]:
                not_subscribed.append(ch)
        except:
            pass
    if not not_subscribed:
        bot.send_message(user_id, "✅ Obuna tasdiqlandi! Endi video yoki rasm havolasini yuboring.")
    else:
        msg = "🚫 Quyidagi kanallarga obuna bo‘lmadingiz:\n" + "\n".join(not_subscribed)
        bot.send_message(user_id, msg)

@bot.message_handler(func=lambda m: m.text and ("instagram.com" in m.text or "tiktok.com" in m.text or "youtube.com" in m.text))
def download_video(message):
    url = message.text.strip()
    bot.send_message(message.chat.id, "⏳ Yuklanmoqda, biroz kuting...")
    try:
        api_url = f"https://save-from.net/api/convert?url={url}"
        response = requests.get(api_url).json()
        if 'url' in response and response['url']:
            video_url = response['url']
            bot.send_video(message.chat.id, video_url, caption="🎥 Videongiz tayyor!")
        else:
            bot.send_message(message.chat.id, "⚠️ Video yuklab bo‘lmadi. Havolani tekshirib qayta urinib ko‘ring.")
    except:
        bot.send_message(message.chat.id, "❌ Yuklashda xatolik yuz berdi.")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id not in ADMINS:
        bot.send_message(message.chat.id, "❌ Siz admin emassiz.")
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📢 Reklama yuborish", "➕ Kanal qo‘shish", "➖ Kanal o‘chirish")
    markup.add("📊 Statistika", "👑 Admin qo‘shish")
    bot.send_message(message.chat.id, "👑 Admin panel:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "📊 Statistika")
def stats(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "📊 Statistika hali ishlab chiqilmoqda...")

@bot.message_handler(func=lambda m: m.text == "📢 Reklama yuborish")
def broadcast(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "✍️ Reklama matnini yuboring:")
        bot.register_next_step_handler(message, send_broadcast)

def send_broadcast(message):
    from db import get_all_users
    users = get_all_users()
    count = 0
    for user in users:
        try:
            bot.send_message(user, message.text)
            count += 1
        except:
            pass
    bot.send_message(message.chat.id, f"✅ {count} ta foydalanuvchiga yuborildi.")

@bot.message_handler(func=lambda m: m.text == "➕ Kanal qo‘shish")
def add_channel_cmd(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "Kanal username ni yuboring (masalan, @kanalnomi):")
        bot.register_next_step_handler(message, save_channel)

def save_channel(message):
    ch = message.text.strip()
    add_channel(ch)
    bot.send_message(message.chat.id, f"✅ {ch} kanal qo‘shildi.")

@bot.message_handler(func=lambda m: m.text == "➖ Kanal o‘chirish")
def remove_channel_cmd(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "O‘chiriladigan kanal username ni yuboring:")
        bot.register_next_step_handler(message, del_channel)

def del_channel(message):
    ch = message.text.strip()
    remove_channel(ch)
    bot.send_message(message.chat.id, f"❌ {ch} kanal o‘chirildi.")

@bot.message_handler(func=lambda m: m.text == "👑 Admin qo‘shish")
def add_admin_cmd(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "Yangi adminning ID raqamini yuboring:")
        bot.register_next_step_handler(message, save_admin)

def save_admin(message):
    new_admin = int(message.text.strip())
    add_admin(new_admin)
    bot.send_message(message.chat.id, f"✅ {new_admin} admin sifatida qo‘shildi.")

bot.polling(non_stop=True)
