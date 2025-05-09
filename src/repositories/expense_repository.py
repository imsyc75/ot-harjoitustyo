import sqlite3
from .base_repository import BaseRepository

class ExpenseRepository(BaseRepository):
    """Luokka, joka käsittelee kulujen tietokanta toimintoja.
    Se perii BaseRepository-luokan yleiset tietokantaoperaatiot.
    """
    def __init__(self):
        """Alustaa ExpenseRepository-olion."""
        super().__init__(table_name="expenses")
    
    def create(self, expense):
        """Tallentaa uuden kulun tietokantaan.
        
        Args:
            expense: Expense-olio, joka sisältää kulun tiedot
            
        Returns:
            True jos tallennus onnistui, muuten False
        """
        try:
            query = """INSERT INTO expenses 
                    (user_id, amount, category, date, description)
                    VALUES (?, ?, ?, ?, ?)"""
            self.execute_query(query, (
                expense.user_id, 
                expense.amount, 
                expense.category, 
                expense.date, 
                expense.description
            ))
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_for_user(self, user_id):
        """Hakee kaikki käyttäjän kulut tietokannasta.
        
        Args:
            user_id: Käyttäjän id
            
        Returns:
            Lista käyttäjän kuluista
        """
        query = """SELECT id, amount, category, date, description
                FROM expenses
                WHERE user_id = ?
                ORDER BY date DESC"""
        return self.fetch_all(query, (user_id,))
    
    def get_by_date_range(self, user_id, start_date, end_date):
        """Hakee käyttäjän kulut tietyltä aikaväliltä.
        
        Args:
            user_id: Käyttäjän id
            start_date: Aloituspäivämäärä
            end_date: Lopetuspäivämäärä
            
        Returns:
            Lista käyttäjän kuluista annetulla aikavälillä
        """
        query = """SELECT id, user_id, amount, category, date, description
                FROM expenses
                WHERE user_id = ? AND date >= ? AND date < ?
                ORDER BY date DESC"""
        return self.fetch_all(query, (user_id, start_date, end_date))
    
    def get_monthly_total(self, user_id, year, month):
        """Laskee käyttäjän kulujen kokonaissumman tietyltä kuukaudelta.
        
        Args:
            user_id: Käyttäjän id
            year: Vuosi
            month: Kuukausi
            
        Returns:
            Kulujen kokonaissumma kyseiseltä kuukaudelta
        """
        start_date = f"{year}-{month:02d}-01"
        
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
            
        end_date = f"{next_year}-{next_month:02d}-01"
        
        query = """SELECT SUM(amount) as total
                FROM expenses
                WHERE user_id = ? AND date >= ? AND date < ?"""
        result = self.fetch_one(query, (user_id, start_date, end_date))
        return result['total'] if result and result['total'] else 0.0
    
    def get_by_id(self, expense_id, user_id):
        """Hakee yksittäisen kulun tietokannasta.
        
        Args:
            expense_id: Kulun id
            user_id: Käyttäjän id (varmistaa, että kulu kuuluu käyttäjälle)
            
        Returns:
            Kulun tiedot tai None jos kulua ei löydy
        """
        query = """SELECT * FROM expenses
                WHERE id = ? AND user_id = ?"""
        return self.fetch_one(query, (expense_id, user_id))
    
    def update(self, expense):
        """Päivittää kulun tiedot tietokantaan.
        
        Args:
            expense: Expense-olio, joka sisältää päivitetyt tiedot
            
        Returns:
            True jos päivitys onnistui, muuten False
        """
        try:
            query = """UPDATE expenses
                    SET amount = ?, category = ?, date = ?, description = ?
                    WHERE id = ? AND user_id = ?"""
            self.execute_query(query, (
                expense.amount, 
                expense.category, 
                expense.date, 
                expense.description, 
                expense.expense_id, 
                expense.user_id
            ))
            return True
        except sqlite3.Error:
            return False
    
    def delete(self, expense_id, user_id):
        """Poistaa kulun tietokannasta.
        
        Args:
            expense_id: Poistettavan kulun id
            user_id: Käyttäjän id (varmistaa, että kulu kuuluu käyttäjälle)
            
        Returns:
            True jos poisto onnistui, muuten False
        """
        try:
            query = "DELETE FROM expenses WHERE id = ? AND user_id = ?"
            self.execute_query(query, (expense_id, user_id))
            return True
        except sqlite3.Error:
            return False
        