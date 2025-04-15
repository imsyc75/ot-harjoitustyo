import tkinter as tk
from tkinter import messagebox
from entities.user import User
from ui.style import Style

class LoginView(tk.Toplevel):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.title("MoneyTrack - Login")
        self.on_login_success = on_login_success

        Style.apply_style(self)

        tk.Label(self, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        login_button = tk.Button(self, text="Login", command=self.handle_login)
        login_button.grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)

        register_button = tk.Button(self, text="Register", command=self.open_register)
        register_button.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.geometry("700x600")
        self.resizable(True, True)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user_obj = User(username)
        user_data = user_obj.find_by_username()
        if user_data is not None:
            if user_data["password"] == password:
                self.on_login_success(username)
                self.destroy()
            else:
                messagebox.showerror("Error", "Username or password is not correct!")
        else:
            messagebox.showerror("Error", "Username does not exsist")

    def open_register(self):
        from .register_view import RegisterView
        RegisterView(self)