import sqlite3

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db
        self.create_tables()

    def create_connection(self):
        conn = sqlite3.connect(self.path_to_db)
        return conn

    def create_tables(self):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_link TEXT
            )''')
            conn.commit()

    def add_user(self, user_id, username):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
            conn.commit()

    def get_users(self):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users")
            return [row[0] for row in cursor.fetchall()]

    def add_channel(self, channel_link):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO channels (channel_link) VALUES (?)", (channel_link,))
            conn.commit()

    def get_channels(self):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT channel_link FROM channels")
            return [row[0] for row in cursor.fetchall()]
