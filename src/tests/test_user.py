import unittest
import sqlite3
from pathlib import Path


from entities.user import User
from database_connection import get_db_connection
class TestUser(unittest.TestCase):
    def setUp(self):
        self.test_db_path = Path("test_moneytrack.db")
        
        self.conn = sqlite3.connect(str(self.test_db_path))
        self.conn.row_factory = sqlite3.Row
        
        self.conn.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
        self.conn.commit()
        
        self.original_get_db_connection = get_db_connection
        
        def mock_get_db_connection():
            conn = sqlite3.connect(str(self.test_db_path))
            conn.row_factory = sqlite3.Row
            return conn
        
        import src.database_connection
        src.database_connection.get_db_connection = mock_get_db_connection
        
        self.conn.execute("DELETE FROM users")
        self.conn.commit()
    
    def tearDown(self):
        import src.database_connection
        src.database_connection.get_db_connection = self.original_get_db_connection
        
        self.conn.close()
        
        if self.test_db_path.exists():
            self.test_db_path.unlink()
    
    def test_create_user_success(self):
        user = User("testuser", "123456")
        result = user.create()
        self.assertTrue(result)
        
        user_data = self.conn.execute("SELECT * FROM users WHERE username = ?", ("testuser",)).fetchone()
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data["username"], "testuser")
        self.assertEqual(user_data["password"], "123456")
    
    def test_create_user_duplicate(self):
        pass
    
    def test_find_by_username_existing(self):
        pass