import telebot
from telebot import types
import requests
import os
from config import BOT_TOKEN, ADMINS, MANDATORY_CHANNELS
from db import add_user, is_admin, add_admin, get_all_users
from keep_alive import keep_alive

bot = telebot.TeleBot(BOT_TOKEN)

def check_subscription(user_id):
    for channel in MANDATORY_CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user.id, message.from_user.username)
    if not check_subscription(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        for channel in MANDATORY_CHANNELS:
            markup.add(types.InlineKeyboardButton(f"📢 Kanalga obuna bo‘lish", url=f"https://t.me/{channel.replace('@', '')}"))
        markup.add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data="check_subs"))
        bot.send_message(message.chat.id, "⚠️ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "✅ Obuna tasdiqlandi! Endi video yoki rasm havolasini yuboring.")

@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subs(call):
    if check_subscription(call.from_user.id):
        bot.edit_message_text("✅ Obuna muvaffaqiyatli tasdiqlandi! Endi video yoki rasm havolasini yuboring.", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "❌ Hali hamma kanallarga obuna bo‘lmadingiz!")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id in ADMINS:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📊 Statistika", "📣 Reklama yuborish")
        markup.add("➕ Admin qo‘shish", "🔙 Chiqish")
        bot.send_message(message.chat.id, "🔧 Admin panelga xush kelibsiz!", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "⛔ Siz admin emassiz.")

@bot.message_handler(func=lambda message: message.text == "🔙 Chiqish")
def exit_admin(message):
    bot.send_message(message.chat.id, "🏠 Bosh menyuga qaytdingiz.", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: message.text == "📊 Statistika")
def stats(message):
    if message.from_user.id in ADMINS:
        users = get_all_users()
        bot.send_message(message.chat.id, f"📈 Foydalanuvchilar soni: {len(users)} ta")

@bot.message_handler(func=lambda message: message.text == "📣 Reklama yuborish")
def send_ads(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "✉️ Reklama matnini yuboring:")
        bot.register_next_step_handler(message, broadcast)

def broadcast(message):
    users = get_all_users()
    sent = 0
    for user in users:
        try:
            bot.send_message(user[0], message.text)
            sent += 1
        except:
            pass
    bot.send_message(message.chat.id, f"✅ Reklama {sent} ta foydalanuvchiga yuborildi.")

@bot.message_handler(func=lambda message: message.text == "➕ Admin qo‘shish")
def add_new_admin(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "🆔 Yangi admin ID raqamini yuboring:")
        bot.register_next_step_handler(message, save_new_admin)

def save_new_admin(message):
    try:
        new_id = int(message.text)
        add_admin(new_id)
        bot.send_message(message.chat.id, f"✅ {new_id} endi admin sifatida qo‘shildi.")
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri ID format.")

@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def handle_video(message):
    if not check_subscription(message.from_user.id):
        bot.send_message(message.chat.id, "⚠️ Avval kanallarga obuna bo‘ling va /start buyrug‘ini bosing.")
        return
    url = message.text.strip()
    bot.send_message(message.chat.id, "⏳ Yuklanmoqda, biroz kuting...")
    try:
        api_url = f"https://api.savefrom.app/info?url={url}"
        response = requests.get(api_url).json()
        if 'url' in response and response['url']:
            video_url = response['url']
            bot.send_video(message.chat.id, video_url)
        else:
            bot.send_message(message.chat.id, "❌ Yuklab bo‘lmadi. Iltimos, boshqa havola yuboring.")
    except:
        bot.send_message(message.chat.id, "⚠️ Xatolik yuz berdi, iltimos qayta urinib ko‘ring.")

keep_alive()
bot.polling(non_stop=True)
