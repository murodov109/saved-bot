import sqlite3

def get_connection():
    return sqlite3.connect("database.db")

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            subscribed INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT,
            name TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)", (user_id, username, first_name))
    conn.commit()
    conn.close()

def get_channels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT channel_id FROM channels")
    channels = cursor.fetchall()
    conn.close()
    return [c[0] for c in channels]

def add_channel(channel_id, name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO channels (channel_id, name) VALUES (?, ?)", (channel_id, name))
    conn.commit()
    conn.close()

def remove_channel(channel_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM channels WHERE channel_id=?", (channel_id,))
    conn.commit()
    conn.close()
