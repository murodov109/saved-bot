import sqlite3

def connect():
    return sqlite3.connect("data.db", check_same_thread=False)

def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        is_admin INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user

def make_admin(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_admin = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_admins():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE is_admin = 1")
    admins = [row[0] for row in cur.fetchall()]
    conn.close()
    return admins

create_tables()
