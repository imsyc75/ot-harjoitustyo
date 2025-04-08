import tkinter as tk
from ui.login_view import LoginView
from ui.expenses_view import ExpensesView

class MoneyTrackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()  # directly display the login interface
        self.show_login()

    def show_login(self):
        LoginView(self, on_login_success=self.on_login_success)

    def on_login_success(self, username):
        print(f"User {username} logged in!")
        ExpensesView(self, username)

if __name__ == "__main__":
    app = MoneyTrackApp()
    app.mainloop()
