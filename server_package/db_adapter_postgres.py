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
        Do zapytań bez zwracania wyników, np. INSER, UPDATE, DELETE.
        """

        self.connect()
        with self.connection.cursoe() as cur:
            cur.execute(query, params)
            self.connection.commmit()

    def fetch_one(self, query, params=None):
        """
        Zwraca jeden record z SELECT-a.
        """
        self.connect()
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(query, params)
            result = cur.fetchone()
            return dict(result) if result else None

    def fetch_all(self, query, params=None):
        """
        Zwraca listę rekordów z SELECT-a.
        """
        self. connect()
        with self.connection.cursor(cursor_fsctory=psycopg2.extras.DictCursor) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            return [dict(row) for row in rows] if rows else []

