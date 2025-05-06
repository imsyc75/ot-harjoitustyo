from repositories.user_repository import UserRepository
from entities.user import User

class UserService:
    """Käyttäjäpalveluluokka, joka tarjoaa korkeamman tason toimintoja käyttäjiin liittyen.
    
    Tämä luokka toimii välikätenä käyttöliittymän ja tietovaraston välillä.
    """
    
    def __init__(self, user_repository=None):
        """Alustaa palvelun.
        
        Args:
            user_repository: UserRepository-olio tai None, jolloin luodaan uusi.
        """
        self._user_repository = user_repository or UserRepository()
        self._current_user = None
    
    def login(self, username, password):
        """Kirjaa käyttäjän sisään.
        
        Args:
            username: Käyttäjänimi
            password: Salasana
            
        Returns:
            True jos kirjautuminen onnistui, muuten False
        """
        user_data = self._user_repository.find_by_username(username)
        
        if not user_data:
            return False
            
        if user_data['password'] != password:
            return False
            
        self._current_user = User.from_database_row(user_data)
        return True
    
    def logout(self):
        """Kirjaa käyttäjän ulos.
        
        Returns:
            True aina
        """
        self._current_user = None
        return True
    
    def get_current_user(self):
        """Palauttaa nykyisen kirjautuneen käyttäjän.
        
        Returns:
            Nykyinen käyttäjä tai None jos ei kirjautunut
        """
        return self._current_user
    
    def register(self, username, password):
        """Rekisteröi uuden käyttäjän.
        
        Args:
            username: Käyttäjänimi
            password: Salasana
            
        Returns:
            True jos rekisteröinti onnistui, muuten False
        """
        if not username or not password:
            return False
            
        existing = self._user_repository.find_by_username(username)
        if existing:
            return False
            
        user = User(username, password)
        created = self._user_repository.create(user)
        
        if created:
            user_data = self._user_repository.find_by_username(username)
            self._current_user = User.from_database_row(user_data)
            return True
            
        return False
