import psycopg2
import psycopg2.extras
from server_package.db_adapter_interface import DatabaseAdapter


class PostgresDBAdapter(DatabaseAdapter):
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        """
        Do zapytań bez zwracania wyników, np. INSERT, UPDATE, DELETE.
        """
        self.connect()
        with self.connection.cursor() as cur:
            cur.execute(query, params)
        self.connection.commit()

    def fetch_one(self, query, params=None):
        """
        Zwraca słownik reprezentujący pojedynczy wiersz (lub None).
        """
        self.connect()
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(query, params)
            row = cur.fetchone()
            return dict(row) if row else None

    def fetch_all(self, query, params=None):
        """
        Zwraca listę słowników (lub pustą listę).
        """
        self.connect()
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows] if rows else []
