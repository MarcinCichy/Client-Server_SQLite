import os
from configparser import ConfigParser


def get_db_adapter():
    """
    Zwraca instancję adaptera bazy danych w zależności od wartości klucza
    'engine' w sekcji [database] pliku 'database.ini'.

    Obsługiwane wartości:
    - engine=postgresql
    - engine=sqlite
    """
    parser = ConfigParser()
    parser.read('database.ini')

    if not parser.has_section('database'):
        raise Exception("No [database] section found in database.ini")

    engine = parser.get('database', 'engine', fallback='postgresql')
    print(f"ENGINE = {engine}")

    if engine == 'postgresql':
        if not parser.has_section('postgresql'):
            raise Exception("No [postgresql] section found in database.ini")
        host = parser.get('postgresql', 'host')
        port = parser.get('postgresql', 'port')
        dbname = parser.get('postgresql', 'dbname')
        user = parser.get('postgresql', 'user')
        password = parser.get('postgresql', 'password')

        from server_package.db_adapter_postgres import PostgresDBAdapter
        return PostgresDBAdapter(host, port, dbname, user, password)

    elif engine == 'sqlite':
        if not parser.has_section('sqlite'):
            raise Exception("No [sqlite] section found in database.ini")
        db_path_relative = parser.get('sqlite', 'db_path')
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir)
        full_path = os.path.join(base_dir, db_path_relative)

        from server_package.db_adapter_sqlite import SQLiteDBAdapter
        return SQLiteDBAdapter(db_path=full_path)
    else:
        raise ValueError(f"Unsupported engine: {engine}")
