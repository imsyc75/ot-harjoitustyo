import unittest
import sqlite3
from pathlib import Path
from entities.user import User
from database_connection import get_db_connection

class TestUser(unittest.TestCase):
    def setUp(self):
        self.test_db_path = Path("test_moneytrack.db")
        if self.test_db_path.exists():
            self.test_db_path.unlink()
        
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
        
        import database_connection
        database_connection.get_db_connection = mock_get_db_connection
        
        self.conn.execute("DELETE FROM users")
        self.conn.commit()
    
    def tearDown(self):
        import database_connection
        database_connection.get_db_connection = self.original_get_db_connection
        
        self.conn.close()
        
        if self.test_db_path.exists():
            self.test_db_path.unlink()
    
    def test_create_user_repeatedly(self):
        '''Whether to return False when creating a user repeatedly'''
        user1 = User("testuser", "654321")
        user1.create()

        user2 = User("testuser", "654321")
        result = user2.create()
        self.assertFalse(result)
    
    def test_find_by_username_existing(self):
        ''''find an existing user by username'''
        user = User("testuser", "654321")
        user.create()

        found_user = user.find_by_username()
        self.assertEqual(found_user["username"], "testuser")
        self.assertEqual(found_user["password"], "654321")