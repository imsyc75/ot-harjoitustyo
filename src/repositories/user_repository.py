import sqlite3
from .base_repository import BaseRepository

class UserRepository(BaseRepository):
    """Luokka, joka käsittelee käyttäjien tietokanta toimintoja.
    Se perii BaseRepository-luokan yleiset tietokantaoperaatiot.
    """
    
    def create(self, user):
        """Tallentaa uuden käyttäjän tietokantaan.
        
        Args:
            user: User-olio, joka sisältää käyttäjän tiedot
            
        Returns:
            True jos tallennus onnistui, muuten False
        """
        try:
            query = "INSERT INTO users (username, password) VALUES (?, ?)"
            self.execute_query(query, (user.username, user.password))
            return True
        except sqlite3.IntegrityError:
            return False
    
    def find_by_username(self, username):
        """Hakee käyttäjän tietokannasta käyttäjänimen perusteella.
        
        Args:
            username: Käyttäjänimi
            
        Returns:
            Käyttäjän tiedot tietueena tai None jos käyttäjää ei löydy
        """
        query = "SELECT * FROM users WHERE username = ?"
        return self.fetch_one(query, (username,))
        