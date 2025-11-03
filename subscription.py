from telebot import TeleBot
from telebot import types
from db import connect

conn, cur = connect()

cur.execute("CREATE TABLE IF NOT EXISTS channels (username TEXT)")
conn.commit()

def add_channel(username):
    cur.execute("INSERT OR IGNORE INTO channels VALUES (?)", (username,))
    conn.commit()

def remove_channel(username):
    cur.execute("DELETE FROM channels WHERE username=?", (username,))
    conn.commit()

def get_channels():
    cur.execute("SELECT username FROM channels")
    return [r[0] for r in cur.fetchall()]

def check_subscription(bot: TeleBot, user_id):
    for channel in get_channels():
        try:
            status = bot.get_chat_member(channel, user_id)
            if status.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

def ask_to_subscribe(bot: TeleBot, chat_id):
    channels = get_channels()
    if not channels:
        return False
    markup = types.InlineKeyboardMarkup()
    for ch in channels:
        markup.add(types.InlineKeyboardButton(f"📢 {ch}", url=f"https://t.me/{ch.replace('@','')}"))
    markup.add(types.InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub"))
    bot.send_message(chat_id, "👇 Quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)
    return True
