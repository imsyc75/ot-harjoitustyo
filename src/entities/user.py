import sqlite3
from database_connection import get_db_connection

class User:
    def __init__(self, username, password=None, user_id=None):
        self.user_id = user_id
        self.username = username
        self.password = password

    def create(self):
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (self.username, self.password)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            if conn:
                conn.close()

    def find_by_username(self):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (self.username,)).fetchone()
        conn.close()
        return user
    