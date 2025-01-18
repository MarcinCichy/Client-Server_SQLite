# import os
# from configparser import ConfigParser
#
#
# def test_db_config(filename='test_database.ini', section='test_postgresql'):
#     print(f"Trying to read config from: {os.path.abspath(filename)}")
#     parser = ConfigParser()
#     parser.read(filename)
#
#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception(f'Section {section} not found in the {filename} file')
#     print(f"File {os.path.abspath(filename)} was read successfully")
#     return db


import os
from configparser import ConfigParser


def test_get_db_adapter():
    """
    Zwraca instancję adaptera bazy danych w zależności od wartości klucza
    'engine' w sekcji [test_database] pliku 'test_database.ini'.

    Obsługiwane wartości:
    - engine=test_postgresql
    - engine=test_sqlite
    """
    parser = ConfigParser()
    parser.read('test_database.ini')

    if not parser.has_section('test_database'):
        raise Exception("No [test_database] section found in test_database.ini")

    engine = parser.get('test_database', 'engine', fallback='test_postgresql')
    print(f"ENGINE = {engine}")

    if engine == 'test_postgresql':
        if not parser.has_section('test_postgresql'):
            raise Exception("No [test_postgresql] section found in test_database.ini")
        host = parser.get('test_postgresql', 'host')
        port = parser.get('test_postgresql', 'port')
        dbname = parser.get('test_postgresql', 'dbname')
        user = parser.get('test_postgresql', 'user')
        password = parser.get('test_postgresql', 'password')

        from server_package.db_adapter_postgres import PostgresDBAdapter
        return PostgresDBAdapter(host, port, dbname, user, password)

    elif engine == 'test_sqlite':
        if not parser.has_section('test_sqlite'):
            raise Exception("No [test_sqlite] section found in test_database.ini")
        db_path_relative = parser.get('test_sqlite', 'db_path')
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir)
        full_path = os.path.join(base_dir, db_path_relative)

        from server_package.db_adapter_sqlite import SQLiteDBAdapter
        return SQLiteDBAdapter(db_path=full_path)
    else:
        raise ValueError(f"Unsupported engine: {engine}")
