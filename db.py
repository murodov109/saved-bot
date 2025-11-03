import sqlite3

def connect():
    return sqlite3.connect("data.db", check_same_thread=False)

def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        username TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER UNIQUE
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

def get_users():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    data = [row[0] for row in cur.fetchall()]
    conn.close()
    return data

def add_channel(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO channels (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

def get_channels():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT username FROM channels")
    data = [row[0] for row in cur.fetchall()]
    conn.close()
    return data

def remove_channel(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM channels WHERE username = ?", (username,))
    conn.commit()
    conn.close()

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
    data = [row[0] for row in cur.fetchall()]
    conn.close()
    return data

create_tables()
