from database_connection import get_db_connection

def drop_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS expenses""")
    cursor.execute("""DROP TABLE IF EXISTS users""")
    conn.commit()

def create_tables(conn):
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
    conn = get_db_connection()
    try:
        drop_tables(conn)
        create_tables(conn)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally: 
        if conn:
            conn.close()

if __name__ == "__main__":
    initialize_database()
    