import tkinter as tk
from ui.login_view import LoginView
from ui.expenses_view import ExpensesView

class MoneyTrackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()

        self.login_window = None
        self.expenses_window = None

        self.show_login()

    def show_login(self):
        self.login_window = LoginView(self, on_login_success=self.on_login_success)
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_login_close)

    def on_login_close(self):
        self.login_window.destroy()
        self.destroy()

    def on_login_success(self, username):
        print(f"User {username} logged in!")
        self.login_window.destroy()
        
        self.expenses_window = ExpensesView(self, username)
        self.expenses_window.protocol("WM_DELETE_WINDOW", self.on_expenses_close)

    def on_expenses_close(self):
        self.expenses_window.destroy()
        self.destroy() 

if __name__ == "__main__":
    app = MoneyTrackApp()
    app.mainloop()
