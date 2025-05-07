class Expense:
    """luokka, joka edustaa käyttäjän kuluja.
    
    Attributes:
        expense_id: Kulun yksilöllinen tunniste.
        user_id: Käyttäjän yksilöllinen tunniste.
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
        
    @staticmethod
    def from_database_row(row):
        """Luo kulu-olion tietokannan rivistä.
        
        Args:
            row: Tietokannan rivi, joka sisältää kulun tiedot.
            
        Returns:
            Expense-olio tai None, jos rivi on tyhjä.
        """
        if not row:
            return None
        return Expense(
            expense_id=row['id'],
            user_id=row['user_id'],
            amount=row['amount'],
            category=row['category'],
            description=row['description'],
            date=row['date'],
        )
    