import sqlite3
from database_connection import get_db_connection

class BaseRepository:
    """Perusluokka tietokantaoperaatioille.
    Tämä luokka tarjoaa yleiset metodit tietokantakyselyiden suorittamiseen
    ja tuloksien hakemiseen. Kaikki repository-luokat perivät tämän luokan.
    """

    def __init__(self, table_name=None):
        """Alustaa repository-olion.
            Args:
            table_name: Tietokantataulun nimi, jota repository käsittelee.
                        Tämä on valinnainen, mutta vaaditaan delete_all-metodin käyttöön."""
        self.get_connection = get_db_connection
        self.table_name = table_name

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

    def delete_all(self):
        """Poistaa kaikki rivit taulusta.

        Returns:
            True jos poisto onnistui, muuten False

        Raises:
            ValueError: Jos table_name ei ole asetettu.
        """
        try:
            query = f"DELETE FROM {self.table_name}"
            self.execute_query(query)
            return True
        except sqlite3.Error:
            return False

    @staticmethod
    def get_month_date_range(year, month):
        """Laskee tietyn kuukauden päivämäärävälin.

        Args:
            year: Vuosi
            month: Kuukausi

        Returns:
            Tuple (start_date, end_date)
        """
        start_date = f"{year}-{month:02d}-01"

        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        end_date = f"{next_year}-{next_month:02d}-01"

        return start_date, end_date
