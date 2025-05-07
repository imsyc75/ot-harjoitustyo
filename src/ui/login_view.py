import tkinter as tk
from tkinter import messagebox
from services.user_service import UserService
from ui.style import Style

class LoginView(tk.Toplevel):
    """Luokka, joka vastaa kirjautumisnäkymästä.
    
    Attributes:
        on_login_open: Callback-funktio, jota kutsutaan onnistuneen kirjautumisen jälkeen.
    """

    def __init__(self, parent, on_login_open):
        """Luokan konstruktori, joka luo uuden kirjautumisnäkymän.
        
        Args:
            parent: Isäntäikkuna, johon tämä näkymä liittyy.
            on_login_open: Callback-funktio, jota kutsutaan onnistuneen kirjautumisen jälkeen.
        """

        super().__init__(parent)
        self.title("MoneyTrack - Login")
        self.on_login_open = on_login_open
        self.user_service = UserService()

        Style.apply_style(self)

        tk.Label(self, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        login_button = Style.create_button(self, text="Login", command=self.handle_login, is_primary=True)
        login_button.grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)

        register_button = Style.create_button(self, text="Register", command=self.open_register, is_primary=True)
        register_button.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.geometry("700x600")
        self.resizable(True, True)

    def handle_login(self):
        """Käsittelee käyttäjän kirjautumisyrityksen.
        
        Tarkistaa käyttäjänimen ja salasanan oikeellisuuden tietokannasta
        ja kutsuu onnistuneen kirjautumisen callback-funktiota, jos
        kirjautumistiedot ovat oikein.
        """

        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.user_service.login(username, password):
            self.on_login_open(username)
            self.destroy()
        else:
                messagebox.showerror("Error", "Username or password is not correct!")

    def open_register(self):
        """Avaa rekisteröitymisnäkymän.
        """
        
        from .register_view import RegisterView
        RegisterView(self)
        