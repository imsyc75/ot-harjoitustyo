from database_connection import get_db_connection
import sqlite3

class Expense:
    def __init__(self, user_id, amount=None, category=None, description=None, date=None, id=None):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def create(self):
        conn = get_db_connection()
        try:
            conn.execute(
                """INSERT INTO expenses (user_id, amount, category, date, description) 
                VALUES (?, ?, ?, ?, ?)""",
                (self.user_id, self.amount, self.category, self.date, self.description)
            )
            return True
        except sqlite3.IntegrityError:
            return False 
        finally:
            if conn:
               conn.close()

    def get_all_for_user(self):
        conn = get_db_connection()
        try:
            expenses = conn.execute(
                """SELECT id, date,amount, category, description 
                FROM expenses 
                WHERE user_id = ? 
                ORDER BY date DESC""", 
                (self.user_id,)
            ).fetchall()
            return expenses
        except sqlite3.Error:
            return []
        finally:
            if conn:
                conn.close()