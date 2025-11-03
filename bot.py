import telebot
from telebot import types
import requests
from config import BOT_TOKEN, ADMINS
from db import add_user
from admin_panel import is_admin, admin_menu, handle_admin_commands
from subscription import check_subscription, ask_to_subscribe
from keep_alive import keep_alive

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    add_user(user_id, message.from_user.username)
    if not ask_to_subscribe(bot, message.chat.id):
        bot.send_message(message.chat.id, "🎬 Havolani yuboring (Instagram, TikTok, YouTube).")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub(call):
    if check_subscription(bot, call.from_user.id):
        bot.send_message(call.message.chat.id, "✅ Tabriklaymiz! Endi video yoki rasm havolasini yuboring.")
    else:
        bot.answer_callback_query(call.id, "❌ Hali barcha kanallarga obuna bo‘lmadingiz.", show_alert=True)

@bot.message_handler(commands=['admin'])
def admin_panel_cmd(message):
    if is_admin(message.from_user.id):
        admin_menu(bot, message.chat.id)
    else:
        bot.send_message(message.chat.id, "❌ Siz admin emassiz.")

@bot.message_handler(func=lambda m: m.text in ["➕ Kanal qo‘shish", "➖ Kanal o‘chirish", "📊 Statistika", "📢 Reklama yuborish"])
def admin_options(message):
    if is_admin(message.from_user.id):
        handle_admin_commands(bot, message)
    else:
        bot.send_message(message.chat.id, "❌ Siz admin emassiz.")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def download_video(message):
    if not check_subscription(bot, message.from_user.id):
        ask_to_subscribe(bot, message.chat.id)
        return
    bot.send_message(message.chat.id, "⏳ Yuklanmoqda, biroz kuting...")
    try:
        url = f"https://api.save-from.net/api/convert?url={message.text}"
        r = requests.get(url, timeout=15).json()
        if "url" in r and r["url"]:
            link = r["url"][0]["url"]
            if any(x in link for x in [".mp4", "video"]):
                bot.send_video(message.chat.id, link, caption="🎬 Video yuklandi!")
            else:
                bot.send_photo(message.chat.id, link, caption="🖼 Rasm yuklandi!")
        else:
            bot.send_message(message.chat.id, "⚠️ Yuklab bo‘lmadi yoki havola noto‘g‘ri.")
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Xatolik, boshqa havola yuboring.")

keep_alive()
bot.polling(non_stop=True)
