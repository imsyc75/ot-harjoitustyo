import sqlite3
from config import DATABASE_FILE_PATH

def get_db_connection():
    """Luo ja palauttaa tietokantayhteyden.
    
    Returns:
        sqlite3.Connection: Yhteys tietokantaan.
    """
    
    connection = sqlite3.connect(DATABASE_FILE_PATH)
    connection.row_factory = sqlite3.Row
    return connection
