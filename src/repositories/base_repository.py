import sqlite3
from database_connection import get_db_connection

class BaseRepository:
    """Perusluokka tietokantaoperaatioille.
    Tämä luokka tarjoaa yleiset metodit tietokantakyselyiden suorittamiseen
    ja tuloksien hakemiseen. Kaikki repository-luokat perivät tämän luokan.
    """
    
    def __init__(self):
        """Alustaa repository-olion."""
        self.get_connection = get_db_connection
    
    def execute_query(self, query, params=None):
        """Suorittaa SQL-kyselyn ja palauttaa tuloksen.
        
        Args:
            query: SQL-kyselylause
            params: Kyselyn parametrit
            
        Returns:
            Kyselyn tulos tai None virheen sattuessa
        """
        conn = self.get_connection()
        try:
            if params:
                result = conn.execute(query, params)
            else:
                result = conn.execute(query)
            conn.commit()
            return result, conn
        except sqlite3.Error:
            if conn:
                conn.close()
            return None, None
                
    def fetch_one(self, query, params=None):
        """Suorittaa kyselyn ja palauttaa yhden tuloksen.
        
        Args:
            query: SQL-kyselylause
            params: Kyselyn parametrit
            
        Returns:
            Yksi tulostietue tai None jos tulosta ei löydy
        """
        result, conn = self.execute_query(query, params)
        try:
            if result:
                return result.fetchone()
            return None
        finally:
            if conn:
                conn.close()
        
    def fetch_all(self, query, params=None):
        """Suorittaa kyselyn ja palauttaa kaikki tulokset.
        
        Args:
            query: SQL-kyselylause
            params: Kyselyn parametrit
            
        Returns:
            Lista tulostietueista tai tyhjä lista jos tuloksia ei löydy
        """
        result, conn = self.execute_query(query, params)
        try:
            if result:
                return result.fetchall()
            return []
        finally:
            if conn:
                conn.close()
    