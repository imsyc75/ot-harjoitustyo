import tkinter as tk
from tkinter import ttk, messagebox
from entities.expenses import Expense
import datetime
from ui.style import Style

class AddExpenseView(tk.Toplevel):
    """Luokka, joka vastaa kulun lisäämisen tai muokkaamisen näkymästä.
    
    Attributes:
        user_id: Käyttäjän yksilöllinen tunniste.
        expense_data: Muokattavan kulun tiedot tai None uuden kulun tapauksessa.
        expense_id: Muokattavan kulun yksilöllinen tunniste tai None uuden kulun tapauksessa.
    """

    def __init__(self, parent, user_id, expense_data=None):
        """Luokan konstruktori, joka luo uuden kulun lisäämis- tai muokkausnäkymän.
        
        Args:
            parent: Isäntäikkuna, johon tämä näkymä liittyy.
            user_id: Käyttäjän yksilöllinen tunniste.
            expense_data: Muokattavan kulun tiedot tai None uuden kulun tapauksessa.
        """

        super().__init__(parent)
        self.title("MoneyTrack - Add New Expense")
        self.user_id = user_id
        self.expense_data = expense_data

        Style.apply_style(self)

        if expense_data:
            self.title("MoneyTrack - Edit Expense")
            self.expense_id = expense_data["id"]
        else:
            self.title("MoneyTrack - Add New Expense")
            self.expense_id = None

        tk.Label(self, text="Amount ($):").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Category:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.categories = ["Food", "Transportation", "Housing", "Entertainment", "Shopping", "Healthcare", "Other"]
        self.category_combobox = ttk.Combobox(self, values=self.categories)
        self.category_combobox.grid(row=1, column=1, padx=10, pady=5)
        self.category_combobox.current(0)

        tk.Label(self, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.date_entry = tk.Entry(self)
        self.date_entry.grid(row=2, column=1, padx=10, pady=5)
        today = datetime.date.today().strftime("%Y-%m-%d")
        self.date_entry.insert(0, today)

        tk.Label(self, text="Description:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.description_entry = tk.Entry(self)
        self.description_entry.grid(row=3, column=1, padx=10, pady=5)

        button_frame = tk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        save_button = Style.create_button(button_frame, text="Save", command=self.save_expense, is_primary=True)
        save_button.pack(side=tk.LEFT, padx=5)

        cancel_button = Style.create_button(button_frame, text="Cancel", command=self.destroy, is_primary=True)
        cancel_button.pack(side=tk.LEFT, padx=5)

        self.geometry("400x250")
        self.resizable(False, False)

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def save_expense(self):
        """Tallentaa kulun tiedot tietokantaan.
        
        Validoi syötetyt tiedot ja tallentaa ne joko uutena kuluna tai päivittää
        olemassa olevan kulun tietoja riippuen siitä, onko kyseessä uusi vai
        muokattava kulu.
        """
        
        amount = self.amount_entry.get()
        category = self.category_combobox.get()
        date = self.date_entry.get()
        description = self.description_entry.get()

        if not amount or not category or not date:
            messagebox.showerror("Error", "Amount, category, and date cannot be empty!")
            return

        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            messagebox.showerror("Error", "Amount must be a positive number!")
            return

        expense = Expense(
            user_id=self.user_id,
            amount=amount,
            category=category,
            date=date,
            description=description
        )

        success = False
        if self.expense_id:
            success = expense.update(self.expense_id)
            message = "Expense updated successfully!"
        else:
            success = expense.create()
            message = "Expense saved successfully!"

        if success:
            messagebox.showinfo("Success", message)
            self.destroy()
        else:
            messagebox.showerror("Error", "Failed to save expense. Please try again.")