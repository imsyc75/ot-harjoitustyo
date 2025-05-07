from datetime import datetime
from repositories.expense_repository import ExpenseRepository
from entities.expenses import Expense

class ExpenseService:
    """Luokka, joka tarjoaa korkeamman tason toimintoja kuluihin liittyen.
    
    Tämä luokka toimii välikätenä käyttöliittymän ja tietovaraston välillä.
    """
    
    def __init__(self, expense_repository=None):
        """Alustaa palvelun.
        
        Args:
            expense_repository: ExpenseRepository-olio tai None, jolloin luodaan uusi.
        """
        self._expense_repository = expense_repository or ExpenseRepository()
    
    def add_expense(self, user_id, amount, category, description=None, date=None):
        """Lisää uuden kulun.
        
        Args:
            user_id: Käyttäjän ID
            amount: Kulun summa
            category: Kulun kategoria
            description: Kulun kuvaus
            date: Kulun päivämäärä, oletuksena tänään
            
        Returns:
            True jos lisäys onnistui, muuten False
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
            
        expense = Expense(
            user_id=user_id,
            amount=amount,
            category=category,
            description=description,
            date=date
        )
        
        return self._expense_repository.create(expense)
    
    def get_user_expenses(self, user_id):
        """Hakee käyttäjän kaikki kulut.
        
        Args:
            user_id: Käyttäjän id
            
        Returns:
            Lista Expense-olioita
        """
        expenses_data = self._expense_repository.get_all_for_user(user_id)
        return [Expense.from_database_row(row) for row in expenses_data]
    
    def get_monthly_report(self, user_id, year, month):
        """Luo kuukausiraportin käyttäjän kuluista.
        
        Args:
            user_id: Käyttäjän ID
            year: Vuosi
            month: Kuukausi
            
        Returns:
            Sanakirja, joka sisältää kokonaissumman, kategoriat ja kulut
        """
        # Kuukauden kokonaissumma
        total = self._expense_repository.get_monthly_total(user_id, year, month)
        
        # Kuukauden päivämääräväli
        start_date = f"{year}-{month:02d}-01"
        
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
            
        end_date = f"{next_year}-{next_month:02d}-01"
        
        # Hae kaikki kulut kuukaudelta
        expenses_data = self._expense_repository.get_by_date_range(
            user_id, start_date, end_date
        )
        expenses = [Expense.from_database_row(row) for row in expenses_data]
        
        return {
            "total": total,
            "expenses": expenses,
        }
    
    def delete_expense(self, user_id, expense_id):
        """Poistaa kulun.
        
        Args:
            user_id: Käyttäjän ID
            expense_id: Kulun ID
            
        Returns:
            True jos poisto onnistui, muuten False
        """
        return self._expense_repository.delete(expense_id, user_id)
    
    def update_expense(self, expense):
        """Päivittää kulun tiedot.
        
        Args:
            expense: Expense-olio, joka sisältää päivitetyt tiedot
            
        Returns:
            True jos päivitys onnistui, muuten False
        """
        return self._expense_repository.update(expense)
    
    def get_expense_by_id(self, user_id, expense_id):
        """Hakee yksittäisen kulun.
        
        Args:
            user_id: Käyttäjän ID
            expense_id: Kulun ID
            
        Returns:
            Expense-olio tai None jos kulua ei löydy
        """
        expense_data = self._expense_repository.get_by_id(expense_id, user_id)
        return Expense.from_database_row(expense_data)
    