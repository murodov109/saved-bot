import telebot
import requests
from telebot import types
from config import TOKEN, ADMIN_ID
from db import create_tables, add_user, get_channels, add_channel, remove_channel
from api_server import start_server
import threading

bot = telebot.TeleBot(TOKEN)

create_tables()

def is_subscribed(user_id):
    channels = get_channels()
    for ch in channels:
        try:
            status = bot.get_chat_member(ch, user_id)
            if status.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

@bot.message_handler(commands=['start'])
def start_message(message):
    add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    channels = get_channels()
    if not channels:
        bot.reply_to(message, "Majburiy obuna kanallari yo‘q. Admin panel orqali qo‘shing.")
        return
    text = "Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:\n\n"
    for ch in channels:
        text += f"➡️ {ch}\n"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data="check_subs"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subscriptions(call):
    if is_subscribed(call.from_user.id):
        bot.send_message(call.message.chat.id, "✅ Obuna tasdiqlandi!\nEndi video yoki rasm havolasini yuboring.")
    else:
        bot.send_message(call.message.chat.id, "🚫 Siz hali barcha kanallarga obuna bo‘lmagansiz!")

@bot.message_handler(func=lambda message: message.text.startswith("https://"))
def download_media(message):
    url = message.text
    bot.send_message(message.chat.id, "⏳ Yuklanmoqda...")

    try:
        r = requests.get(f"https://api.sssinstagram.com/api/download?url={url}")
        data = r.json()
        if 'url' in data:
            file_url = data['url']
            bot.send_video(message.chat.id, file_url)
        else:
            bot.send_message(message.chat.id, "Video yuklab bo‘lmadi.")
    except:
        bot.send_message(message.chat.id, "Xatolik yuz berdi. Havolani tekshirib qayta urinib ko‘ring.")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("➕ Kanal qo‘shish", callback_data="add_channel"))
    markup.add(types.InlineKeyboardButton("➖ Kanal o‘chirish", callback_data="remove_channel"))
    bot.send_message(message.chat.id, "Admin panel:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["add_channel", "remove_channel"])
def handle_admin_actions(call):
    if call.from_user.id != ADMIN_ID:
        return
    if call.data == "add_channel":
        bot.send_message(call.message.chat.id, "Kanal usernameni yuboring: (masalan, @kanalim)")
        bot.register_next_step_handler(call.message, add_new_channel)
    elif call.data == "remove_channel":
        bot.send_message(call.message.chat.id, "O‘chiriladigan kanal usernameni yuboring:")
        bot.register_next_step_handler(call.message, delete_channel)

def add_new_channel(message):
    add_channel(message.text, message.text)
    bot.send_message(message.chat.id, "✅ Kanal qo‘shildi!")

def delete_channel(message):
    remove_channel(message.text)
    bot.send_message(message.chat.id, "❌ Kanal o‘chirildi!")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=start_server).start()
run_bot()
