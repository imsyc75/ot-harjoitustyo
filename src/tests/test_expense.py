import unittest
import sqlite3
from pathlib import Path
import database_connection
from entities.expenses import Expense
from database_connection import get_db_connection

class TestExpense(unittest.TestCase):
    def setUp(self):
        self.test_db_path = Path("test_moneytrack.db")
        if self.test_db_path.exists():
            self.test_db_path.unlink()
        
        self.conn = sqlite3.connect(str(self.test_db_path))
        self.conn.row_factory = sqlite3.Row
        
        self.conn.execute("""
        CREATE TABLE expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        self.conn.commit()
        
        self.original_get_db_connection = get_db_connection
        
        def mock_get_db_connection():
            conn = sqlite3.connect(str(self.test_db_path))
            conn.row_factory = sqlite3.Row
            return conn
        
        import database_connection
        database_connection.get_db_connection = mock_get_db_connection

        self.conn.execute("DELETE FROM expenses")
        self.conn.commit()

    def tearDown(self):
        database_connection.get_db_connection = self.original_get_db_connection
        
        self.conn.close()
        
        if self.test_db_path.exists():
            self.test_db_path.unlink()

    def test_create_and_get_expense(self):
        conn = get_db_connection()
        conn.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()

        expense = Expense(
            user_id=1,
            amount=100.50,
            category="food",
            date="2025-04-07",
            description=""
        )
        
        self.assertTrue(expense.create())

        expenses = expense.get_all_for_user()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]['amount'], 100.50)
        self.assertEqual(expenses[0]['category'], "food")
        self.assertEqual(expenses[0]['date'], "2025-04-07")
        self.assertEqual(expenses[0]['description'], "")
        
        expense_id = expenses[0]['id']
        fetched_expense = expense.get_by_id(expense_id)
        self.assertIsNotNone(fetched_expense)
        self.assertEqual(fetched_expense['amount'], 100.50)
        self.assertEqual(fetched_expense['user_id'], 1)

    def test_update_expense(self):
        conn = get_db_connection()
        conn.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()

        expense = Expense(
            user_id=1,
            amount=200.00,
            category="Transportation",
            date="2025-04-06",
            description="taxi"
        )
        
        self.assertTrue(expense.create())
        
        expenses = expense.get_all_for_user()
        self.assertEqual(len(expenses), 1)
        expense_id = expenses[0]['id']
        
        updated_expense = Expense(
            user_id=1,
            amount=250.00,
            category="Transportation",
            date="2025-04-06",
            description="taxi and parking"
        )
        self.assertTrue(updated_expense.update(expense_id))

        fetched_expense = expense.get_by_id(expense_id)
        self.assertEqual(fetched_expense['amount'], 250.00)
        self.assertEqual(fetched_expense['description'], "taxi and parking")

    def test_delete_expense(self):
        conn = get_db_connection()
        conn.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()

        expense = Expense(
            user_id=1,
            amount=50.75,
            category="Entertaiment",
            date="2025-04-05",
            description="film ticket"
        )

        self.assertTrue(expense.create())

        expenses = expense.get_all_for_user()
        self.assertEqual(len(expenses), 1)
        expense_id = expenses[0]['id']

        self.assertTrue(expense.delete(expense_id))

        expenses_after_delete = expense.get_all_for_user()
        self.assertEqual(len(expenses_after_delete), 0)
        
        fetched_expense = expense.get_by_id(expense_id)
        self.assertIsNone(fetched_expense)

    def test_get_expenses_by_date_range(self):
        conn = get_db_connection()
        conn.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()

        expense1 = Expense(
        user_id=1,
        amount=100.00,
        category="Food",
        date="2025-04-01",
        description="Groceries"
        )
        expense1.create()

        expense2 = Expense(
        user_id=1,
        amount=50.00,
        category="Entertainment",
        date="2025-04-15",
        description="Movie"
        ) 
        expense2.create()

        expense3 = Expense(
        user_id=1,
        amount=75.25,
        category="Transportation",
        date="2025-05-05",
        description="Gas"
        )
        expense3.create()

        expense4 = Expense(
        user_id=2,
        amount=200.00,
        category="Food",
        date="2025-04-10",
        description="Restaurant"
        )
        expense4.create()

        expense = Expense(user_id=1)
    
        april_expenses = expense.get_expenses_by_date_range("2025-04-01", "2025-05-01")
        self.assertEqual(len(april_expenses), 2)
        self.assertEqual(april_expenses[0]['amount'], 50.00)  
        self.assertEqual(april_expenses[1]['amount'], 100.00)
    
        may_expenses = expense.get_expenses_by_date_range("2025-05-01", "2025-06-01")
        self.assertEqual(len(may_expenses), 1)
        self.assertEqual(may_expenses[0]['amount'], 75.25)
       
        march_expenses = expense.get_expenses_by_date_range("2025-03-01", "2025-04-01") 
        self.assertEqual(len(march_expenses), 0)
    
    def test_get_monthly_total(self):
        conn = get_db_connection()
        conn.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()

        expense1 = Expense(
        user_id=1,
        amount=100.00,
        category="Food",
        date="2025-04-01",
        description="Groceries"
        )
        expense1.create()

        expense2 = Expense(
        user_id=1,
        amount=50.00,
        category="Entertainment",
        date="2025-04-15",
        description="Movie"
        )
        expense2.create()

        expense3 = Expense(
        user_id=1,
        amount=75.50,
        category="Transportation",
        date="2025-05-05",
        description="Gas"
        )
        expense3.create()

        expense4 = Expense(
        user_id=1,
        amount=125.75,
        category="Shopping",
        date="2025-05-20",
        description="Clothes"
        )
        expense4.create()

        expense5 = Expense(
        user_id=2,
        amount=200.00,
        category="Food",
        date="2025-04-10",
        description="Restaurant"
        )
        expense5.create()

        expense = Expense(user_id=1)

        april_total = expense.get_monthly_total(2025, 4)
        self.assertEqual(april_total, 150.00)  # 100 + 50
    
        may_total = expense.get_monthly_total(2025, 5)
        self.assertEqual(may_total, 201.25)  # 75.50 + 125.75
    
        june_total = expense.get_monthly_total(2025, 6)
        self.assertEqual(june_total, 0.0)
