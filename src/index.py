import tkinter as tk
from ui.login_view import LoginView
from ui.expenses_view import ExpensesView

class MoneyTrackApp(tk.Tk):
    """Luokka, joka hallinnoi koko sovellusta.
    
    Luokka vastaa sovellusikkunoiden vaihtamisesta ja hallinnasta.
    """

    def __init__(self):
        """Luokan konstruktori, joka alustaa sovelluksen.
        """

        super().__init__()
        self.withdraw()

        self.login_window = None
        self.expenses_window = None

        self.show_login()

    def show_login(self):
        """Näyttää kirjautumisnäkymän.
        
        Tuhoaa mahdolliset aiemmat ikkunat ja luo uuden kirjautumisikkunan.
        """
                
        if self.login_window and self.login_window.winfo_exists():
            self.login_window.destroy()

        if self.expenses_window and self.expenses_window.winfo_exists():
            self.expenses_window.destroy()

        self.login_window = LoginView(self, on_login_open=self.on_login_open)
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_login_close)

    def on_login_close(self):
        """Käsittelee kirjautumisikkunan sulkemisen.
        
        Tuhoaa kirjautumisikkunan ja sulkee sovelluksen.
        """
                
        self.login_window.destroy()
        self.destroy()

    def on_login_open(self, username):
        """Käsittelee onnistuneen kirjautumisen.
        
        Tuhoaa kirjautumisikkunan ja luo kulunhallintanäkymän.
        
        Args:
            username: Kirjautuneen käyttäjän käyttäjänimi.
        """
                
        print(f"User {username} logged in!")
        if self.login_window and self.login_window.winfo_exists():
            self.login_window.destroy()
        self.expenses_window = ExpensesView(self, username)
        self.expenses_window.protocol("WM_DELETE_WINDOW", self.on_expenses_close)

    def on_expenses_close(self):
        """Käsittelee kulunhallintaikkunan sulkemisen.
        
        Tuhoaa kulunhallintaikkunan ja sulkee sovelluksen.
        """
                
        if self.expenses_window and self.expenses_window.winfo_exists():
            self.expenses_window.destroy()
        self.destroy()

if __name__ == "__main__":
    app = MoneyTrackApp()
    app.mainloop()
    