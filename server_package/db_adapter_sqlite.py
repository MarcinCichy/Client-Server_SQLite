import sqlite3
from server_package.db_adapter_interface import DatabaseAdapter


class SQLiteDBAdapter(DatabaseAdapter):
    def __init__(self, db_path):
        """
        db_path -> ścieżka do bazy SQLite, np. "my_database.db"
        """
        self.db_path = db_path
        self.connection = None

    def connect(self):
        if not self.connection:
            # self.connection = sqlite3.connect(self.db_path)
            self.connection = sqlite3.connect(self.db_path,
                                              detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            # row_factory -> obiekt sqlite3.Row
            self.connection.row_factory = sqlite3.Row

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        """
        Zapytania bez zwracania wyników (INSERT, UPDATE, DELETE).
        """
        self.connect()
        query = query.replace('%s', '?')  # zamiana placeholderów
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params or [])

    def fetch_one(self, query, params=None):
        """
        Zwraca słownik (jeden wiersz) lub None.
        """
        self.connect()
        query = query.replace('%s', '?')
        cursor = self.connection.cursor()
        cursor.execute(query, params or [])
        row = cursor.fetchone()
        if not row:
            return None
        # row to sqlite3.Row -> słownik
        return dict(row)

    def fetch_all(self, query, params=None):
        """
        Zwraca listę słowników lub pustą listę.
        """
        self.connect()
        query = query.replace('%s', '?')
        cursor = self.connection.cursor()
        cursor.execute(query, params or [])
        rows = cursor.fetchall()
        return [dict(r) for r in rows] if rows else []
