import sqlite3

def connect():
    return sqlite3.connect("data.db", check_same_thread=False)

def create_tables():
    db = connect()
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS admins (admin_id INTEGER PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS channels (channel TEXT PRIMARY KEY)")
    db.commit()
    db.close()

def add_user(user_id, username):
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    db.commit()
    db.close()

def get_users():
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    db.close()
    return users

def add_admin(admin_id):
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT OR IGNORE INTO admins (admin_id) VALUES (?)", (admin_id,))
    db.commit()
    db.close()

def get_admins():
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT admin_id FROM admins")
    admins = [row[0] for row in cursor.fetchall()]
    db.close()
    return admins

def add_channel(channel):
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT OR IGNORE INTO channels (channel) VALUES (?)", (channel,))
    db.commit()
    db.close()

def remove_channel(channel):
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM channels WHERE channel=?", (channel,))
    db.commit()
    db.close()

def get_channels():
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT channel FROM channels")
    channels = [row[0] for row in cursor.fetchall()]
    db.close()
    return channels

create_tables()
