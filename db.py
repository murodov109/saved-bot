import sqlite3

def connect():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor

def create_tables():
    conn, cursor = connect()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        username TEXT,
        is_admin INTEGER DEFAULT 0
    )""")
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn, cursor = connect()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def get_users():
    conn, cursor = connect()
    cursor.execute("SELECT user_id, username, is_admin FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def add_admin(user_id):
    conn, cursor = connect()
    cursor.execute("UPDATE users SET is_admin = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def remove_admin(user_id):
    conn, cursor = connect()
    cursor.execute("UPDATE users SET is_admin = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def is_admin(user_id):
    conn, cursor = connect()
    cursor.execute("SELECT is_admin FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == 1
