from database_connection import get_db_connection
import sqlite3

class User:
    def __init__(self, username, password=None, id=None):
        self.id = id
        self.username = username
        self.password = password 

    def create(self):
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)",(self.username, self.password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False 
        finally:
            conn.close()

    def find_by_username(self):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (self.username,)).fetchone()
        conn.close()
        return user