import tkinter as tk
import datetime
from tkinter import ttk, messagebox
from entities.expenses import Expense
from ui.add_expenses_view import AddExpenseView
from ui.style import Style

class ExpensesView(tk.Toplevel):
    """Luokka, joka vastaa käyttäjän kulujen näyttämisestä ja hallinnasta.
    
    Näkymä sisältää kulujen listauksen, suodatusmahdollisuudet sekä toiminnot
    kulujen lisäämiseen, muokkaamiseen ja poistamiseen.
    
    Attributes:
        user_id: Kirjautuneen käyttäjän yksilöllinen tunniste.
        parent: Isäntäikkuna, johon tämä näkymä liittyy.
        current_date: Nykyinen päivämäärä.
        current_month: Valittu kuukausi suodatukseen.
        current_year: Valittu vuosi suodatukseen.
    """

    def __init__(self, parent, user_id):
        """Luokan konstruktori, joka luo uuden kulunhallinnan päänäkymän.
        
        Args:
            parent: Isäntäikkuna, johon tämä näkymä liittyy.
            user_id: Kirjautuneen käyttäjän yksilöllinen tunniste.
        """

        super().__init__(parent)
        self.title("MoneyTrack - Expenses")
        self.user_id = user_id
        self.parent = parent

        Style.apply_style(self)

        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        self.current_date = datetime.date.today()
        self.current_month = self.current_date.month
        self.current_year = self.current_date.year

        tk.Label(top_frame, text="choose the month:").pack(side=tk.LEFT, padx=5, pady=5)
        self.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        self.month_var = tk.StringVar()
        self.month_combobox = ttk.Combobox(top_frame, textvariable=self.month_var,
                                           values=self.months, width=5)
        self.month_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.month_combobox.current(self.current_month - 1)  # set to current month

        tk.Label(top_frame, text="year:").pack(side=tk.LEFT, padx=5, pady=5)
        self.year_var = tk.StringVar(value=str(self.current_year))
        self.year_entry = tk.Entry(top_frame, textvariable=self.year_var, width=6)
        self.year_entry.pack(side=tk.LEFT, padx=5, pady=5)

        search_button = tk.Button(top_frame, text="Search", command=self.filter_expenses)
        search_button.pack(side=tk.LEFT, padx=10, pady=5)

        logout_button = tk.Button(top_frame, text="Logout", command=self.logout)
        logout_button.pack(side=tk.RIGHT, padx=10, pady=5)

        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        add_button = tk.Button(button_frame, text="Add New Expense", command=self.open_add_expense)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.expenses_frame = tk.Frame(self)
        self.expenses_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.expenses_tree = ttk.Treeview(self.expenses_frame,
                    columns=("ID", "Amount", "Category", "Date", "Description"), show="headings")
        self.expenses_tree.heading("ID", text="ID")
        self.expenses_tree.heading("Amount", text="Amount")
        self.expenses_tree.heading("Category", text="Category")
        self.expenses_tree.heading("Date", text="Date")
        self.expenses_tree.heading("Description", text="Description")

        self.expenses_tree.column("ID", width=50)
        self.expenses_tree.column("Amount", width=100)
        self.expenses_tree.column("Category", width=150)
        self.expenses_tree.column("Date", width=100)
        self.expenses_tree.column("Description", width=300)

        scrollbar = ttk.Scrollbar(self.expenses_frame, orient=tk.VERTICAL, command=self.expenses_tree.yview)
        self.expenses_tree.configure(yscroll=scrollbar.set)

        self.expenses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        action_frame = tk.Frame(self)
        action_frame.pack(fill=tk.X, padx=10, pady=5)

        edit_button = tk.Button(action_frame, text="Edit Selected", command=self.edit_selected_expense)
        edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(action_frame, text="Delete Selected", command=self.delete_selected_expense)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.summary_frame = tk.Frame(self)
        self.summary_frame.pack(fill=tk.X, padx=10, pady=10)

        self.total_label = tk.Label(self.summary_frame, text="This month you spend: $0.00",
                                   font=("Arial", 14, "bold"))
        self.total_label.pack(side=tk.RIGHT, padx=15, pady=5)

        self.load_expenses()

        self.geometry("700x600")
        self.resizable(True, True)

    def logout(self):
        """Käsittelee käyttäjän uloskirjautumisen.
        
        Vahvistaa uloskirjautumisen käyttäjältä ja palauttaa sovelluksen
        kirjautumisnäkymään, jos käyttäjä vahvistaa toiminnon.
        """

        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
        if confirm:
            self.destroy()
            self.parent.show_login()

    def filter_expenses(self):
        """Suodattaa kulut valitun kuukauden ja vuoden perusteella.
        
        Tarkistaa annettujen arvojen kelpoisuuden ja päivittää näkymän
        vastaamaan valittua aikaväliä.
        """

        try:
            selected_month = self.month_combobox.current() + 1
            selected_year = int(self.year_var.get())

            if selected_year < 1900 or selected_year > 2100:
                messagebox.showerror("Wrong", "Please enter year between 1900-2100")
                return

            self.current_month = selected_month
            self.current_year = selected_year
            self.load_expenses()

        except ValueError:
            messagebox.showerror("Wrong", "Please enter valid year!")

    def load_expenses(self):
        """Lataa käyttäjän kulut tietokannasta ja päivittää näkymän.
        
        Hakee kulut valitulta kuukaudelta, päivittää kulutaulukon sekä
        kuukauden kokonaiskulujen summan.
        """

        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)

        start_date = f"{self.current_year}-{self.current_month:02d}-01"

        if self.current_month == 12:
            next_month = 1
            next_year = self.current_year + 1
        else:
            next_month = self.current_month + 1
            next_year = self.current_year

        end_date = f"{next_year}-{next_month:02d}-01"

        expense_obj = Expense(user_id=self.user_id)
        expenses = expense_obj.get_expenses_by_date_range(start_date, end_date)

        total_expenses = 0.0

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
                    expense["id"],
                    f"${expense['amount']:.2f}",
                    expense["category"],
                    expense["date"],
                    expense["description"]
                ))
                total_expenses += expense["amount"]
            self.total_label.config(text=f"This month you spend: ${total_expenses:.2f}")

    def open_add_expense(self):
        """Avaa uuden kulun lisäämisen näkymän.
        
        Odottaa näkymän sulkemista ja päivittää kulutaulukon.
        """
                
        add_view = AddExpenseView(self, self.user_id)
        self.wait_window(add_view)
        self.load_expenses()

    def get_selected_expense_id(self):
        """Hakee valitun kulun tunnisteen.
        
        Returns:
            Valitun kulun tunniste tai None, jos mitään kulua ei ole valittu.
        """

        selected_items = self.expenses_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select an expense first")
            return None

        item_values = self.expenses_tree.item(selected_items[0], "values")
        if not item_values:
            return None

        return item_values[0]

    def delete_selected_expense(self):
        """Poistaa valitun kulun.
        
        Varmistaa toiminnon käyttäjältä ja poistaa kulun tietokannasta,
        jos käyttäjä vahvistaa toiminnon.
        """
                
        expense_id = self.get_selected_expense_id()
        if not expense_id:
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?")
        if not confirm:
            return

        expense_obj = Expense(user_id=self.user_id)
        if expense_obj.delete(expense_id):
            messagebox.showinfo("Success", "Expense deleted successfully")
            self.load_expenses()
        else:
            messagebox.showerror("Error", "Failed to delete expense. Please try again.")

    def edit_selected_expense(self):
        """Avaa valitun kulun muokkausnäkymän.
        
        Hakee valitun kulun tiedot tietokannasta ja avaa muokkausnäkymän.
        Odottaa näkymän sulkemista ja päivittää kulutaulukon.
        """
        
        expense_id = self.get_selected_expense_id()
        if not expense_id:
            return

        expense_obj = Expense(user_id=self.user_id)
        expense_data = expense_obj.get_by_id(expense_id)

        if not expense_data:
            messagebox.showerror("Error", "Could not find the selected expense")
            return

        edit_view = AddExpenseView(self, self.user_id, expense_data)
        self.wait_window(edit_view)
        self.load_expenses()
