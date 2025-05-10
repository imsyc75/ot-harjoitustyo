import unittest
from datetime import datetime
from services.expense_service import ExpenseService
from repositories.expense_repository import ExpenseRepository
from entities.expenses import Expense

class TestExpenseService(unittest.TestCase):
    def setUp(self):
        self.expense_repository = ExpenseRepository()

        self.expense_repository.delete_all()

        self.expense_service = ExpenseService(self.expense_repository)

        self.test_user_id = 1
        self.test_amount = 100.50
        self.test_category = "Food"
        self.test_description = "Lunch"
        self.test_date = "2025-05-10"

    def test_add_expense(self):
        result = self.expense_service.add_expense(
            self.test_user_id,
            self.test_amount,
            self.test_category,
            self.test_description,
            self.test_date
        )

        self.assertTrue(result)

        expenses = self.expense_service.get_user_expenses(self.test_user_id)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].user_id, self.test_user_id)
        self.assertEqual(expenses[0].amount, self.test_amount)
        self.assertEqual(expenses[0].category, self.test_category)
        self.assertEqual(expenses[0].description, self.test_description)
        self.assertEqual(expenses[0].date, self.test_date)

    def test_add_expense_with_default_date(self):
        result = self.expense_service.add_expense(
            self.test_user_id,
            self.test_amount,
            self.test_category,
            self.test_description
        )

        self.assertTrue(result)

        expenses = self.expense_service.get_user_expenses(self.test_user_id)
        self.assertEqual(len(expenses), 1)

        today = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(expenses[0].date, today)

    def test_add_expense_when_create_fails(self):
        # ExpenseRepository aliluokka
        class FailingCreateExpenseRepository(ExpenseRepository):
            def create(self, expense):
                return False

        failing_repository = FailingCreateExpenseRepository()
        expense_service = ExpenseService(failing_repository)

        result = expense_service.add_expense(
            self.test_user_id,
            self.test_amount,
            self.test_category
        )

        self.assertFalse(result)

    def test_get_user_expenses(self):
        self.expense_service.add_expense(
            self.test_user_id, 100, "Food", "Lunch", "2025-05-01"
        )
        self.expense_service.add_expense(
            self.test_user_id, 200, "Housing", "2025-05-05"
        )
        self.expense_service.add_expense(
            self.test_user_id, 50, "Entertainment", "film ticket", "2025-05-10"
        )

        expenses = self.expense_service.get_user_expenses(self.test_user_id)

        self.assertEqual(len(expenses), 3)

        for expense in expenses:
            self.assertIsInstance(expense, Expense)

    def test_get_user_expenses_empty(self):
        expenses = self.expense_service.get_user_expenses(999)

        self.assertEqual(len(expenses), 0)

    def test_get_monthly_report(self):
        self.expense_service.add_expense(
            self.test_user_id, 100, "ruoka", "Lounas", "2025-04-15"
        )
        self.expense_service.add_expense(
            self.test_user_id, 200, "Housing", "2025-05-05"
        )
        self.expense_service.add_expense(
            self.test_user_id, 50, "Entertainment", "film ticket", "2025-05-15"
        )
        self.expense_service.add_expense(
            self.test_user_id, 300, "Shopping", "clothes", "2025-06-01"
        )

        report = self.expense_service.get_monthly_report(self.test_user_id, 2025, 5)

        self.assertEqual(report["total"], 250)  # 200 + 50

        self.assertEqual(len(report["expenses"]), 2)

        categories = [expense["category"] for expense in report["expenses"]]
        self.assertIn("Housing", categories)
        self.assertIn("Entertainment", categories)

    def test_get_monthly_report_december_edge_case(self):
        self.expense_service.add_expense(
            self.test_user_id, 100, "Food", "Dinner", "2024-12-25"
        )

        report = self.expense_service.get_monthly_report(self.test_user_id, 2024, 12)

        self.assertEqual(report["total"], 100)
        self.assertEqual(len(report["expenses"]), 1)

    def test_delete_expense(self):
        self.expense_service.add_expense(
            self.test_user_id,
            self.test_amount,
            self.test_category,
            self.test_description,
            self.test_date
        )

        expenses = self.expense_service.get_user_expenses(self.test_user_id)
        expense_id = expenses[0].expense_id

        result = self.expense_service.delete_expense(self.test_user_id, expense_id)

        self.assertTrue(result)

        expenses_after = self.expense_service.get_user_expenses(self.test_user_id)
        self.assertEqual(len(expenses_after), 0)

    def test_delete_expense_nonexistent(self):
        result = self.expense_service.delete_expense(self.test_user_id, 9999)

        self.assertFalse(result)

    def test_update_expense(self):
        self.expense_service.add_expense(
            self.test_user_id,
            self.test_amount,
            self.test_category,
            self.test_description,
            self.test_date
        )

        expenses = self.expense_service.get_user_expenses(self.test_user_id)
        expense_id = expenses[0].expense_id

        updated_expense = {
            "expense_id": expense_id,
            "user_id": self.test_user_id,
            "amount": 150.75,
            "category": "Entertainment",
            "description": "film ticket",
            "date": "2025-05-15"
        }

        result = self.expense_service.update_expense(updated_expense)

        self.assertTrue(result)

        updated = self.expense_service.get_expense_by_id(self.test_user_id, expense_id)
        self.assertEqual(updated.amount, 150.75)
        self.assertEqual(updated.category, "Entertainment")
        self.assertEqual(updated.description, "film ticket")
        self.assertEqual(updated.date, "2025-05-15")

    def test_update_expense_when_update_fails(self):
        # # se on ExpenseRepository aliluokka
        class FailingUpdateExpenseRepository(ExpenseRepository):
            def update(self, expense):
                return False

        failing_repository = FailingUpdateExpenseRepository()
        expense_service = ExpenseService(failing_repository)

        updated_expense = {
            "expense_id": 1,
            "user_id": self.test_user_id,
            "amount": 150.75,
            "category": "Entertainment",
            "description": "Elokuvalippu",
            "date": "2025-05-15"
        }

        result = expense_service.update_expense(updated_expense)

        self.assertFalse(result)

    def test_get_expense_by_id(self):
        self.expense_service.add_expense(
            self.test_user_id,
            self.test_amount,
            self.test_category,
            self.test_description,
            self.test_date
        )

        expenses = self.expense_service.get_user_expenses(self.test_user_id)
        expense_id = expenses[0].expense_id

        expense = self.expense_service.get_expense_by_id(self.test_user_id, expense_id)

        self.assertEqual(expense.expense_id, expense_id)
        self.assertEqual(expense.user_id, self.test_user_id)
        self.assertEqual(expense.amount, self.test_amount)
        self.assertEqual(expense.category, self.test_category)
        self.assertEqual(expense.description, self.test_description)
        self.assertEqual(expense.date, self.test_date)

    def test_get_expense_by_id_nonexistent(self):
        # ExpenseRepository aliluokka
        class NonexistentExpenseRepository(ExpenseRepository):
            def get_by_id(self, expense_id, user_id):
                return None

        nonexistent_repository = NonexistentExpenseRepository()
        expense_service = ExpenseService(nonexistent_repository)

        try:
            expense_service.get_expense_by_id(self.test_user_id, 9999)
            self.fail("Should throw an exception")
        except:
            pass

if __name__ == '__main__':
    unittest.main()
    