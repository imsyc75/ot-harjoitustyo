from database_connection import get_db_connection

def drop_tables(conn):
    """Poistaa tietokannan taulut, jos ne ovat olemassa.
    
    Args:
        conn: Tietokantayhteys.
    """

    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS expenses""")
    cursor.execute("""DROP TABLE IF EXISTS users""")
    conn.commit()

def create_tables(conn):
    """Luo tietokannan taulut.
    
    Args:
        conn: Tietokantayhteys.
    """
        
    cursor = conn.cursor()
    # generoitu koodi alkaa
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    # generoitu koodi päättyy
    conn.commit()

def initialize_database():
    """Alustaa tietokannan poistamalla vanhat taulut ja luomalla uudet.
    """
    
    conn = get_db_connection()
    drop_tables(conn)
    create_tables(conn)
    print("Database tables created successfully")
    if conn:
        conn.close()

if __name__ == "__main__":
    initialize_database()
    