import sqlite3
from database_connection import get_db_connection


class Expense:
    def __init__(self, user_id, amount=None, category=None, description=None,
                 date=None, expense_id=None):
        self.expense_id = expense_id
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
            conn.commit()
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
                """SELECT id, amount, category, date, description
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

    def delete(self, expense_id):
        conn = get_db_connection()
        try:
            conn.execute(
                "DELETE FROM expenses WHERE id = ? AND user_id = ?",
                (expense_id, self.user_id)
            )
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            if conn:
                conn.close()

    def get_by_id(self, expense_id):
        conn = get_db_connection()
        try:
            expense = conn.execute(
                """SELECT * FROM expenses
                WHERE id = ? AND user_id = ?""",
                (expense_id, self.user_id)
            ).fetchone()
            return expense
        except sqlite3.Error:
            return None
        finally:
            if conn:
                conn.close()

    def update(self, expense_id):
        conn = get_db_connection()
        try:
            conn.execute(
                """UPDATE expenses
                SET amount = ?, category = ?, date = ?, description = ?
                WHERE id = ? AND user_id = ?""",
                (self.amount, self.category, self.date, self.description, expense_id, self.user_id)
            )
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            if conn:
                conn.close()
