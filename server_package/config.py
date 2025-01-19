import os
from configparser import ConfigParser


def get_db_adapter():
    """
    Zwraca instancję adaptera bazy danych w zależności od wartości klucza 'engine'
    w sekcji [database] pliku konfiguracyjnego.

    Jeśli TEST_ENV jest ustawione na 'test', konfiguracja jest pobierana z 'test_database.ini',
    w przeciwnym razie z 'database.ini'.

    Obsługiwane wartości:
      - engine=postgresql – odczytuje parametry z sekcji [postgresql] i tworzy PostgresDBAdapter
      - engine=sqlite – odczytuje parametry z sekcji [sqlite] i tworzy SQLiteDBAdapter
    """
    # Wybierz plik konfiguracyjny w zależności od zmiennej środowiskowej
    config_file = 'test_database.ini' if os.getenv('TEST_ENV') == 'test' else 'database.ini'

    parser = ConfigParser()
    read_files = parser.read(config_file)
    if not read_files:
        raise Exception(f"Nie udało się odczytać pliku konfiguracyjnego: {config_file}")

    if not parser.has_section('database'):
        raise Exception(f"No [database] section found in {config_file}")

    # Możesz też zdecydować, czy chcesz przyjmować silnik z konfiguracji, czy też wymuszać
    # np. TEST_ENGINE na podstawie zmiennej środowiskowej.
    engine = os.getenv("TEST_ENGINE", parser.get('database', 'engine', fallback='postgresql'))
    print(f"ENGINE = {engine}")

    # Obsługa PostgreSQL
    if engine == 'postgresql':
        if not parser.has_section('postgresql'):
            raise Exception(f"No [postgresql] section found in {config_file}")
        host = parser.get('postgresql', 'host')
        port = parser.get('postgresql', 'port')
        dbname = parser.get('postgresql', 'dbname')
        user = parser.get('postgresql', 'user')
        password = parser.get('postgresql', 'password')

        from server_package.db_adapter_postgres import PostgresDBAdapter
        return PostgresDBAdapter(host, port, dbname, user, password)

    # Obsługa SQLite
    elif engine == 'sqlite':
        if not parser.has_section('sqlite'):
            raise Exception(f"No [sqlite] section found in {config_file}")
        db_path_relative = parser.get('sqlite', 'db_path')
        # Jeśli chcesz, aby folder db_files pozostawał w głównym katalogu projektu,
        # a plik config.py znajduje się w server_package, możesz zrobić tak:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir)
        full_path = os.path.join(base_dir, db_path_relative)
        print(f"FULL_PATH = {full_path}")

        from server_package.db_adapter_sqlite import SQLiteDBAdapter
        return SQLiteDBAdapter(db_path=full_path)

    else:
        raise ValueError(f"Unsupported engine: {engine}")
