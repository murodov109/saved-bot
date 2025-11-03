import sqlite3

class Database:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT)")
            cur.execute("CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT)")
            cur.execute("CREATE TABLE IF NOT EXISTS admins (admin_id INTEGER PRIMARY KEY)")
            conn.commit()

    def add_user(self, user_id, username):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
            conn.commit()

    def get_users(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT user_id FROM users")
            users = [row[0] for row in cur.fetchall()]
        return users

    def add_channel(self, username):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO channels (username) VALUES (?)", (username,))
            conn.commit()

    def remove_channel(self, username):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM channels WHERE username = ?", (username,))
            conn.commit()

    def get_channels(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT username FROM channels")
            channels = [row[0] for row in cur.fetchall()]
        return channels

    def add_admin(self, admin_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("INSERT OR IGNORE INTO admins (admin_id) VALUES (?)", (admin_id,))
            conn.commit()

    def get_admins(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT admin_id FROM admins")
            admins = [row[0] for row in cur.fetchall()]
        return admins
