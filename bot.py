import telebot
from telebot import types
from downloader import download_media
from api_server import keep_alive
from config import BOT_TOKEN
from db import add_user

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user.id, message.from_user.username)
    bot.send_message(message.chat.id, "👋 Salom! Havolani yuboring (Instagram, TikTok, YouTube, Twitter, Pinterest).")

@bot.message_handler(func=lambda msg: msg.text.startswith("http"))
def handle_link(message):
    bot.send_message(message.chat.id, "⏳ Yuklanmoqda, biroz kuting...")
    data = download_media(message.text)
    if not data:
        bot.send_message(message.chat.id, "⚠️ Xatolik, havola noto‘g‘ri yoki yuklab bo‘lmadi.")
        return
    if data["type"] == "video":
        bot.send_video(message.chat.id, data["url"], caption="🎬 Video yuklandi!")
    elif data["type"] == "photo":
        bot.send_photo(message.chat.id, data["url"], caption="🖼 Rasm yuklandi!")
    elif data["type"] == "link":
        bot.send_message(message.chat.id, f"🎥 Videoni yuklash uchun link:\n{data['url']}")
    else:
        bot.send_message(message.chat.id, "❌ Yuklab bo‘lmadi, boshqa havola yuboring.")

keep_alive()
bot.polling(non_stop=True)
