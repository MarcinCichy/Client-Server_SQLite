import os
from configparser import ConfigParser


def test_get_db_config(filename='test_database.ini'):
    """
    Zwraca konfigurację testową jako słownik, np.:
      {'engine': 'postgresql', 'host': '127.0.0.1', 'port': '5432', 'dbname': 'test_db_CS', 'user': 'postgres', 'password': 'MC'}
      lub dla SQLite: {'engine': 'sqlite', 'db_path': 'db_files/test_db_CS_SQLite.db'}
    """
    parser = ConfigParser()
    parser.read(filename)

    if not parser.has_section('database'):
        raise Exception(f"No [database] section found in {filename}")

    engine = parser.get('database', 'engine', fallback='postgresql').lower()
    config = {"engine": engine}

    if engine == 'postgresql':
        if not parser.has_section('postgresql'):
            raise Exception(f"No [postgresql] section found in {filename}")
        config.update(dict(parser.items('postgresql')))
    elif engine == 'sqlite':
        if not parser.has_section('sqlite'):
            raise Exception(f"No [sqlite] section found in {filename}")
        config.update(dict(parser.items('sqlite')))
    else:
        raise ValueError(f"Unsupported engine: {engine}")

    return config


def get_db_adapter():
    """
    Zwraca instancję adaptera bazy danych na podstawie konfiguracji.
    """
    config = test_get_db_config()
    engine = config['engine']
    if engine == 'postgresql':
        from server_package.db_adapter_postgres import PostgresDBAdapter
        return PostgresDBAdapter(
            host=config['host'],
            port=config['port'],
            dbname=config['dbname'],
            user=config['user'],
            password=config['password']
        )
    elif engine == 'sqlite':
        from server_package.db_adapter_sqlite import SQLiteDBAdapter
        db_path = config['db_path']
        if not os.path.isabs(db_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, db_path)
            print(f"DB_PATH = {db_path}")
        return SQLiteDBAdapter(db_path=db_path)
    else:
        raise ValueError(f"Unsupported engine: {engine}")
