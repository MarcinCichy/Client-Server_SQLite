import os
from configparser import ConfigParser


def get_db_adapter():
    """
    Zwraca instancję adpatera bazy danych w zależności od wartości klucza 'engine w sekcji [datbase] pliku 'database.ini'.

    Obsługiwane wartoci:
    - engine=postgresql - odczytuje parametry z sekcji [postgresql] i tworzy PostgresDBAdapter
    - engine=sqlite - odczytuje parametry z sekcji [sqlite] i tworzy SQLiteDBAdapter
    """

    parser = ConfigParser()
    parser.read('database.ini')

    if not parser.has_section('database'):
        raise Exception("No [database] section found in database.ini file")

    engine = parser.get('database', 'engine', fallback='postgresql')

    # --------------------------
    #  Obsługa PostgreSQL
    # --------------------------
    if engine == 'postgresql':
        if not parser.has_section('postgresql'):
            raise Exception("No [postgresql] section found in database.ini file")
        # Odczyt parametrów z sekcji [postgresql]
        host = parser.get('postgresql', 'host')
        port = parser.get('postgresql', 'port')
        dbname = parser.get('postgresql', 'dbname')
        user = parser.get('postgresql', 'user')
        password = parser.get('postgresql', 'password')

        from server_package.db_adapter_postgres import PostgresDBAdapter
        return PostgresDBAdapter(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
    # --------------------------
    #  Obsługa SQLite
    # --------------------------
    elif engine == 'sqlite':
        if not parser.has_section('sqlite'):
            raise Exception("No [sqlite] section found in database.ini file")
        # Odczyt parametrów z sekcji [sqlite]
        db_path = parser.get('sqlite', 'db_path')

        from server_package.db_adapter_sqlite import SQLiteDBAdapter
        return SQLiteDBAdapter(db_path=db_path)
    # --------------------------
    #  Obsługa nieznanego silnika
    # --------------------------
    else:
        raise ValueError(f"Unsupported engine: {engine}")
