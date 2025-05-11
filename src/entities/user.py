class User:
    """Luokka, joka edustaa sovelluksen käyttäjää.

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

    @staticmethod
    def from_database_row(row):
        """Luo käyttäjäolion tietokannan rivistä.

        Args:
            row: Tietokannan rivi, joka sisältää käyttäjän tiedot.

        Returns:
            User-olio tai None, jos rivi on tyhjä.
        """
        if not row:
            return None
        return User(
            username=row['username'],
            password=row['password'],
            user_id=row['id']
        )
