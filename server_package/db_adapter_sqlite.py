import sqlite3
from server_package.db_adapter_interface import DatabaseAdapter


class SQLiteDBAdapter(DatabaseAdapter):
    def __init__(self, db_path):
        """
        db_path -> ścieżka dostępu do bazy SQLite, np. "my_database.db
        """
        self.db_path = db_path
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params= None):
        self.connect()
        with self.connection:
            cursor = self.connection.cursor()
            query = query.replace('%s', '?')
            cursor.execute(query, params or [])

    def fetch_one(self, query, params=None):
        self.connect()
        cursor = self.connection.cursor()
        query = query.replace('%s', '?')
        cursor.execute(query, params or [])
        row = cursor.fetchone()
        if row:
            return row
        return None

    def fetch_all(self, query, params=None):
        self.connect()
        cursor = self.connection.cursor()
        query = query.replace('%s', '?')
        cursor.execute(query, params or [])
        rows = cursor.fetchall()
        return rows if rows else []

