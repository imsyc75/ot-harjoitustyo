import tkinter as tk
from tkinter import messagebox
from services.user_service import UserService
from ui.style import Style

class RegisterView(tk.Toplevel):
    """Luokka, joka vastaa käyttäjän rekisteröitymisnäkymästä.
    """

    def __init__(self, parent):
        """Luokan konstruktori, joka luo uuden rekisteröitymisnäkymän.
        
        Args:
            parent: Isäntäikkuna, johon tämä näkymä liittyy.
        """

        super().__init__(parent)
        self.title("MoneyTrack - Register")
        self.user_service = UserService()

        Style.apply_style(self)

        tk.Label(self, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        register_button = Style.create_button(self, text="Submit", command=self.handle_register, is_primary=True)
        register_button.grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)

        self.geometry("700x600")
        self.resizable(True, True)

    def handle_register(self):
        """Käsittelee käyttäjän rekisteröitymisen.
        
        Tarkistaa syötettyjen tietojen kelpoisuuden ja tallentaa uuden käyttäjän 
        tietokantaan. Ilmoittaa käyttäjälle rekisteröitymisen onnistumisesta 
        tai epäonnistumisesta.
        """
        
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty!")
            return
        
        if self.user_service.register(username, password):
            messagebox.showinfo("Success", f"User {username} registered!")
            self.destroy()
        else:
            messagebox.showerror("Error", "Username already exists!")
            