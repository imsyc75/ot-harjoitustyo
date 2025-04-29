import sqlite3
from database_connection import get_db_connection

class Expense:
    """Luokka, jonka avulla käsitellään kulutietoja.

    Attributes:
        expense_id: Kulun yksilöllinen tunniste.
        user_id: Käyttäjän yksilöllinen tunniste, johon kulu liittyy.
        amount: Kulun summa.
        category: Kulun kategoria.
        description: Kulun kuvaus.
        date: Kulun päivämäärä.
    """

    def __init__(self, user_id, amount=None, category=None, description=None,
                 date=None, expense_id=None):
        """Luokan konstruktori, joka luo uuden kulun.

        Args:
            user_id: Käyttäjän yksilöllinen tunniste.
            amount: Kulun summa.
            category: Kulun kategoria.
            description: Kulun kuvaus.
            date: Kulun päivämäärä.
            expense_id: Kulun yksilöllinen tunniste.
        """

        self.expense_id = expense_id
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def create(self):
        """Tallentaa uuden kulun tietokantaan.

        Returns:
            True, jos tallennus onnistui, muussa tapauksessa False.
        """

        conn = get_db_connection()
        try:
            conn.execute(
                """INSERT INTO expenses (user_id, amount, category, date, description)
                VALUES (?, ?, ?, ?, ?)""",
                (self.user_id, self.amount, self.category, self.date, self.description)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            if conn:
                conn.close()

    def get_all_for_user(self):
        """Hakee kaikki käyttäjän kulut tietokannasta.

        Returns:
            Lista käyttäjän kuluista järjestettynä päivämäärän mukaan laskevasti.
        """

        conn = get_db_connection()
        try:
            expenses = conn.execute(
                """SELECT id, amount, category, date, description
                FROM expenses
                WHERE user_id = ?
                ORDER BY date DESC""",
                (self.user_id,)
            ).fetchall()
            return expenses
        except sqlite3.Error:
            return []
        finally:
            if conn:
                conn.close()

    def get_expenses_by_date_range(self, start_date, end_date):
        """Hakee käyttäjän kulut tietyltä aikaväliltä.

        Args:
            start_date (str): Aikavälin aloituspäivämäärä muodossa YYYY-MM-DD.
            end_date (str): Aikavälin lopetuspäivämäärä muodossa YYYY-MM-DD.

        Returns:
            Lista käyttäjän kuluista annetulla aikavälillä
            järjestettynä päivämäärän mukaan laskevasti.
        """

        conn = get_db_connection()
        try:
            expenses = conn.execute(
                """SELECT id, amount, category, date, description
                FROM expenses
                WHERE user_id = ? AND date >= ? AND date < ?
                ORDER BY date DESC""",
                (self.user_id, start_date, end_date)
            ).fetchall()
            return expenses
        except sqlite3.Error:
            return []
        finally:
            if conn:
                conn.close()

    def get_monthly_total(self, year, month):
        """Laskee käyttäjän kulujen kokonaissumman tietyltä kuukaudelta.

        Args:
            year (int): Vuosi.
            month (int): Kuukausi.

        Returns:
            float: Kulujen kokonaissumma kyseiseltä kuukaudelta.
        """

        start_date = f"{year}-{month:02d}-01"

        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        end_date = f"{next_year}-{next_month:02d}-01"

        conn = get_db_connection()
        try:
            result = conn.execute(
                """SELECT SUM(amount) as total
                FROM expenses
                WHERE user_id = ? AND date >= ? AND date < ?""",
                (self.user_id, start_date, end_date)
            ).fetchone()

            return result['total'] if result['total'] else 0.0
        except sqlite3.Error:
            return 0.0
        finally:
            if conn:
                conn.close()

    def delete(self, expense_id):
        """Poistaa kulun tietokannasta.

        Args:
            expense_id: Poistettavan kulun yksilöllinen tunniste.

        Returns:
            True, jos poisto onnistui, muussa tapauksessa False.
        """

        conn = get_db_connection()
        try:
            conn.execute(
                "DELETE FROM expenses WHERE id = ? AND user_id = ?",
                (expense_id, self.user_id)
            )
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            if conn:
                conn.close()

    def get_by_id(self, expense_id):
        """Hakee yksittäisen kulun tietokannasta tunnisteen perusteella.

        Args:
            expense_id: Haettavan kulun yksilöllinen tunniste.

        Returns:
            Kulun tiedot tai None, jos kulua ei löydy.
        """

        conn = get_db_connection()
        try:
            expense = conn.execute(
                """SELECT * FROM expenses
                WHERE id = ? AND user_id = ?""",
                (expense_id, self.user_id)
            ).fetchone()
            return expense
        except sqlite3.Error:
            return None
        finally:
            if conn:
                conn.close()

    def update(self, expense_id):
        """Päivittää kulun tiedot tietokantaan.

        Args:
            expense_id: Päivitettävän kulun yksilöllinen tunniste.

        Returns:
            True, jos päivitys onnistui, muussa tapauksessa False.
        """

        conn = get_db_connection()
        try:
            conn.execute(
                """UPDATE expenses
                SET amount = ?, category = ?, date = ?, description = ?
                WHERE id = ? AND user_id = ?""",
                (self.amount, self.category, self.date, self.description, expense_id, self.user_id)
            )
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            if conn:
                conn.close()
