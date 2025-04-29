import sqlite3
from database_connection import get_db_connection

class User:
    """Luokka, jonka avulla käsitellään käyttäjätietoja.

        Attributes:
        user_id: Käyttäjän yksilöllinen tunniste.
        username: Käyttäjän käyttäjänimi.
        password: Käyttäjän salasana.
    """

    def __init__(self, username, password=None, user_id=None):
        """Luokan konstruktori, joka luo uuden käyttäjän.

        Args:
            username: Käyttäjän käyttäjänimi.
            password: Käyttäjän salasana.
            user_id: Käyttäjän yksilöllinen tunniste.
        """

        self.user_id = user_id
        self.username = username
        self.password = password

    def create(self):
        """Tallentaa uuden käyttäjän tietokantaan.

        Returns:
            True, jos tallennus onnistui, muussa tapauksessa False.
        """

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (self.username, self.password)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            if conn:
                conn.close()

    def find_by_username(self):
        """Hakee käyttäjän tietokannasta käyttäjänimen perusteella.

        Returns:
            Käyttäjän tiedot.
        """

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (self.username,)).fetchone()
        conn.close()
        return user
