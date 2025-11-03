import sqlite3

def connect():
    return sqlite3.connect("data.db", check_same_thread=False)

def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE, username TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY AUTOINCREMENT, admin_id INTEGER UNIQUE)")
    cur.execute("CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY AUTOINCREMENT, channel_username TEXT UNIQUE)")
    conn.commit()
    conn.close()

def add_user(user_id, username=None):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def get_users():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    data = [r[0] for r in cur.fetchall()]
    conn.close()
    return data

def add_admin(admin_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO admins (admin_id) VALUES (?)", (admin_id,))
    conn.commit()
    conn.close()

def get_admins():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT admin_id FROM admins")
    data = [r[0] for r in cur.fetchall()]
    conn.close()
    return data

def add_channel(channel_username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO channels (channel_username) VALUES (?)", (channel_username,))
    conn.commit()
    conn.close()

def remove_channel(channel_username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM channels WHERE channel_username = ?", (channel_username,))
    conn.commit()
    conn.close()

def get_channels():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT channel_username FROM channels")
    data = [r[0] for r in cur.fetchall()]
    conn.close()
    return data

create_tables()
