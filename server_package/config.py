import os
from configparser import ConfigParser


def db_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db


def get_db_adapter():
    """
    Zwraca instancję adpatera bazy danych w zależności od wartości klucza 'engine w sekcji [datbase].

    """
    parser =ConfigParser()
    parser.read('database.ini')

    if not parser.has_section('database'):
        raise Exception("No [database] section found in database.ini file")

    engine = parser.get('database', 'engine', fallback='postgres')

    if engine == 'postgres':
        # Odczyt parametrów z sekcji [postgresql]
        params = db_config(section='postgresql')
        from server_package.db_adapter_postgres import PostgresDBAdapter
        return PostgresDBAdapter(
            host=params['host'],
            port=params['port'],
            dbname=params['dbname'],
            user=params['user'],
            password=params['password']
        )
    elif engine == 'sqlite':
        # Odczyt parametrów z sekcji [sqlite]
        params = db_config(section='sqlite')
        from server_package.db_adapter_sqlite import SQLiteDBAdapter
        return SQLiteDBAdapter(db_path=params['db_path'])
    else:
        raise ValueError(f"Unsupported engine: {engine}")
