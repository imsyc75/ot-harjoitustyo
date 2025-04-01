import tkinter as tk
from ui.login_view import LoginView

class MoneyTrackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()  # directly display the login interface
        self.show_login()

    def show_login(self):
        LoginView(self, on_login_success=self.on_login_success)

    def on_login_success(self, username):
        print(f"User {username} logged in!")
        self.deiconify()  # Display the main window (to be implemented)

if __name__ == "__main__":
    app = MoneyTrackApp()
    app.mainloop()