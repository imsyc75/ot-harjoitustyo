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

    def get_expenses_by_date_range(self, start_date, end_date):
        """Get expenses within a specified date range
        Args:
            start_date (str): YYYY-MM-DD
            end_date (str): YYYY-MM-DD
        Returns:
            list: the list of expenses
        """
        conn = get_db_connection()
        try:
            expenses = conn.execute(
                """SELECT id, amount, category, date, description
                FROM expenses
                WHERE user_id = ? AND date >= ? AND date < ?
                ORDER BY date DESC""",
                (self.user_id, start_date, end_date)
            ).fetchall()
            return expenses
        except sqlite3.Error:
            return []
        finally:
            if conn:
                conn.close()

    def get_monthly_total(self, year, month):
        """Get expenses within a specified month
        Args:
            year (int)
            month (int)
        Returns:
            float: the total expenses amout
        """
        start_date = f"{year}-{month:02d}-01"

        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        end_date = f"{next_year}-{next_month:02d}-01"

        conn = get_db_connection()
        try:
            result = conn.execute(
                """SELECT SUM(amount) as total
                FROM expenses
                WHERE user_id = ? AND date >= ? AND date < ?""",
                (self.user_id, start_date, end_date)
            ).fetchone()

            return result['total'] if result['total'] else 0.0
        except sqlite3.Error:
            return 0.0
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
