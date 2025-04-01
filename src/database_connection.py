import sqlite3
import os
from pathlib import Path

# The database file will be saved in the 'data' folder in the project root directory
def get_database_path():
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True) 
    return str(data_dir / "moneytrack.db")

def get_db_connection():
    conn = sqlite3.connect(get_database_path())
    conn.row_factory = sqlite3.Row 
    return conn