import tkinter as tk
from tkinter import ttk, messagebox
from entities.expenses import Expense
from ui.add_expenses_view import AddExpenseView

class ExpensesView(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.title(f"MoneyTrack - Expenses")
        self.user_id = user_id
        
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        add_button = tk.Button(button_frame, text="Add New Expense", command=self.open_add_expense)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.expenses_frame = tk.Frame(self)
        self.expenses_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.expenses_tree = ttk.Treeview(self.expenses_frame, columns=("Amount", "Category", "Date", "Description"), show="headings")
        self.expenses_tree.heading("Amount", text="Amount")
        self.expenses_tree.heading("Category", text="Category")
        self.expenses_tree.heading("Date", text="Date")
        self.expenses_tree.heading("Description", text="Description")

        self.expenses_tree.column("Amount", width=100)
        self.expenses_tree.column("Category", width=150)
        self.expenses_tree.column("Date", width=100)
        self.expenses_tree.column("Description", width=300)
        
        scrollbar = ttk.Scrollbar(self.expenses_frame, orient=tk.VERTICAL, command=self.expenses_tree.yview)
        self.expenses_tree.configure(yscroll=scrollbar.set)
        
        self.expenses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_expenses()

        self.geometry("700x600")
        self.resizable(True, True)
    
    def load_expenses(self):
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)
        
        expense_obj = Expense(user_id=self.user_id)
        expenses = expense_obj.get_all_for_user()
        
        if not expenses:
            message_label = tk.Label(self.expenses_frame, text="You don't have any expenses yet", font=("Arial", 14))
            message_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            # generoitu koodi alkaa
            for widget in self.expenses_frame.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget("text") == "You don't have any expenses yet":
                    widget.destroy()
            # generoitu koodi päättyy

            for expense in expenses:
                self.expenses_tree.insert("", tk.END, values=(
                    f"${expense['amount']:.2f}",
                    expense["category"],
                    expense["date"],
                    expense["description"]
                ))
    
    def open_add_expense(self):
        add_view = AddExpenseView(self, self.user_id)
        self.wait_window(add_view)
        self.load_expenses()