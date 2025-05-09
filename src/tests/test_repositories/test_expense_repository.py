import unittest
from repositories.expense_repository import ExpenseRepository
from entities.expenses import Expense

expense_repository = ExpenseRepository()

class TestExpenseRepository(unittest.TestCase):
    def setUp(self):
        expense_repository.delete_all()

        self.user_id = 1
        self.expense1 = Expense(
            user_id=self.user_id,
            amount=100.50,
            category="Food",
            date="2025-05-01",
        )
        self.expense2 = Expense(
            user_id=self.user_id,
            amount=200.75,
            category="Transportation",
            date="2025-05-15",
            description="HSL"
        )
        self.expense3 = Expense(
            user_id=self.user_id,
            amount=150.25,
            category="Shopping",
            date="2025-06-01",
            description="clothes"
        )

        self.other_user_id = 2
        self.other_user_expense = Expense(
            user_id=self.other_user_id,
            amount=75.00,
            category="Food",
            date="2025-05-10",
            description="dinner"
        )

    def test_create(self):
        result = expense_repository.create(self.expense1)

        self.assertTrue(result)
        expenses = expense_repository.get_all_for_user(self.user_id)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["amount"], self.expense1.amount)
        self.assertEqual(expenses[0]["category"], self.expense1.category)
        self.assertEqual(expenses[0]["date"], self.expense1.date)
        self.assertEqual(expenses[0]["description"], self.expense1.description)

    def test_get_all_for_user(self):
        expense_repository.create(self.expense1)
        expense_repository.create(self.expense2)
        expense_repository.create(self.other_user_expense)

        expenses = expense_repository.get_all_for_user(self.user_id)

        self.assertEqual(len(expenses), 2)
        self.assertEqual(expenses[0]["date"], self.expense2.date)
        self.assertEqual(expenses[1]["date"], self.expense1.date)

    def test_get_by_date_range(self):
        expense_repository.create(self.expense1)  # 2025-05-01
        expense_repository.create(self.expense2)  # 2025-05-15
        expense_repository.create(self.expense3)  # 2025-06-01

        start_date = "2025-05-01"
        end_date = "2025-06-01"
        expenses = expense_repository.get_by_date_range(self.user_id, start_date, end_date)

        self.assertEqual(len(expenses), 2)
        self.assertEqual(expenses[0]["date"], self.expense2.date)
        self.assertEqual(expenses[1]["date"], self.expense1.date)

    def test_get_monthly_total(self):
        expense_repository.create(self.expense1)  # 2025-05-01, 100.50
        expense_repository.create(self.expense2)  # 2025-05-15, 200.75
        expense_repository.create(self.expense3)  # 2025-06-01, 150.25
        expense_repository.create(self.other_user_expense)

        may_total = expense_repository.get_monthly_total(self.user_id, 2025, 5)
        june_total = expense_repository.get_monthly_total(self.user_id, 2025, 6)

        self.assertEqual(may_total, 100.50 + 200.75)
        self.assertEqual(june_total, 150.25)

    def test_get_monthly_total_no_expenses(self):
        total = expense_repository.get_monthly_total(self.user_id, 2025, 7)
        self.assertEqual(total, 0.0)

    def test_get_by_id(self):
        expense_repository.create(self.expense1)
        expenses = expense_repository.get_all_for_user(self.user_id)
        expense_id = expenses[0]["id"]

        found_expense = expense_repository.get_by_id(expense_id, self.user_id)

        self.assertIsNotNone(found_expense)
        self.assertEqual(found_expense["amount"], self.expense1.amount)
        self.assertEqual(found_expense["category"], self.expense1.category)

    def test_get_by_id_not_found(self):
        found_expense = expense_repository.get_by_id(999, self.user_id)
        self.assertIsNone(found_expense)

    def test_get_by_id_wrong_user(self):
        expense_repository.create(self.other_user_expense)
        expenses = expense_repository.get_all_for_user(self.other_user_id)
        expense_id = expenses[0]["id"]

        found_expense = expense_repository.get_by_id(expense_id, self.user_id)
        self.assertIsNone(found_expense)

    def test_update(self):
        expense_repository.create(self.expense1)
        expenses = expense_repository.get_all_for_user(self.user_id)
        expense_id = expenses[0]["id"]

        updated_expense = Expense(
            expense_id=expense_id,
            user_id=self.user_id,
            amount=120.00,
            category="Housing",
            date="2025-05-02",
        )

        result = expense_repository.update(updated_expense)

        self.assertTrue(result)
        found_expense = expense_repository.get_by_id(expense_id, self.user_id)
        self.assertEqual(found_expense["amount"], 120.00)
        self.assertEqual(found_expense["category"], "Housing")
        self.assertEqual(found_expense["date"], "2025-05-02")

    def test_delete(self):
        expense_repository.create(self.expense1)
        expenses = expense_repository.get_all_for_user(self.user_id)
        expense_id = expenses[0]["id"]

        result = expense_repository.delete(expense_id, self.user_id)

        self.assertTrue(result)
        expenses_after_delete = expense_repository.get_all_for_user(self.user_id)
        self.assertEqual(len(expenses_after_delete), 0)

if __name__ == '__main__':
    unittest.main()
