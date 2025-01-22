import os
import time
from tests.unit.test_config import test_get_db_config

# Pobieramy konfigurację testową jako słownik.
config = test_get_db_config()
engine = config.get("engine", "postgresql").lower()

if engine == 'postgresql':
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    temp_db_name = config['dbname']
    default_db = 'postgres'


    def create_temp_db():
        try:
            # Łączymy się do domyślnej bazy, aby utworzyć tymczasową bazę
            conn = psycopg2.connect(
                dbname=default_db,
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password']
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE {temp_db_name};")
            cur.close()
            conn.close()
            time.sleep(2)
            print(f"PostgreSQL: Database {temp_db_name} created successfully.")

            # Tworzymy tabele w testowej bazie
            conn_temp = psycopg2.connect(
                dbname=temp_db_name,
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password']
            )
            cur_temp = conn_temp.cursor()
            cur_temp.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id serial PRIMARY KEY,
                    user_name varchar(50) NOT NULL UNIQUE,
                    permissions varchar(5) NOT NULL,
                    status varchar(6) NOT NULL,
                    activation_date date NOT NULL,
                    login_time timestamp without time zone
                );
            """)
            cur_temp.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    message_id serial PRIMARY KEY,
                    sender_id varchar(50),
                    date date NOT NULL,
                    recipient_id varchar(50) REFERENCES users(user_name) ON DELETE CASCADE,
                    content varchar(250)
                );
            """)
            cur_temp.execute("""
               CREATE TABLE IF NOT EXISTS passwords (
                   user_id integer NOT NULL,
                   hashed_password bytea NOT NULL,
                   salt bytea NOT NULL,
                   PRIMARY KEY (user_id),
                   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
               );
            """)
            conn_temp.commit()
            cur_temp.close()
            conn_temp.close()
            print("PostgreSQL: Testing database with tables was created.")
        except Exception as e:
            print(f"An error occurred while creating the PostgreSQL database: {e}")


    def drop_temp_db():
        try:
            conn = psycopg2.connect(
                dbname=default_db,
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password']
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            # Zabijamy wszystkie aktywne połączenia z testową bazą
            cur.execute(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{temp_db_name}'
                  AND pid <> pg_backend_pid();
            """)
            cur.execute(f"DROP DATABASE IF EXISTS {temp_db_name};")
            cur.close()
            conn.close()
            print("PostgreSQL: Testing database was dropped.")
            time.sleep(2)
        except Exception as e:
            print(f"An error occurred while dropping the PostgreSQL database: {e}")


    def fill_temp_db():
        try:
            print("PostgreSQL: Test tables filling was started.")
            conn = psycopg2.connect(
                dbname=temp_db_name,
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password']
            )
            cur = conn.cursor()

            users_data = [
                ("user1", "admin", "active", "2024-02-18"),
                ("user2", "user", "banned", "2024-02-18"),
                ("user3", "user", "active", "2024-02-18"),
                ("user4", "admin", "active", "2024-02-18"),
                ("user5", "user", "banned", "2024-02-18")
            ]
            import bcrypt
            passwords = ["password1", "password2", "password3", "password4", "password5"]
            for idx, user_data in enumerate(users_data):
                cur.execute("""
                    INSERT INTO users (user_name, permissions, status, activation_date)
                    VALUES (%s, %s, %s, %s) RETURNING user_id
                """, user_data)
                user_id = cur.fetchone()[0]
                password = passwords[idx].encode('utf-8')
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                cur.execute("""
                    INSERT INTO passwords (user_id, hashed_password, salt)
                    VALUES (%s, %s, %s)
                """, (user_id, hashed_password, hashed_password[:29]))

            messages_data = [
                ("user1", "2024-02-18", "user1", "Hello, user2!"),
                ("user2", "2024-02-18", "user2", "Hi there, user3!"),
                ("user1", "2024-02-18", "user3", "Hey user4, how are you?"),
                ("user4", "2024-02-18", "user1", "Greetings, user5!"),
                ("user4", "2024-02-18", "user5", "Welcome, user1!"),
                ("user2", "2024-02-18", "user1", "Hello, user2!"),
                ("user3", "2024-02-18", "user1", "Hello, user2!"),
                ("user5", "2024-02-18", "user1", "Hello, user2!")
            ]
            for message_data in messages_data:
                cur.execute("""
                    INSERT INTO messages (sender_id, date, recipient_id, content)
                    VALUES (%s, %s, %s, %s)
                """, message_data)

            conn.commit()
            cur.close()
            conn.close()
            print("PostgreSQL: Test tables filling was finished.")
        except Exception as e:
            print(f"An error occurred while filling the PostgreSQL database: {e}")

elif engine == 'sqlite':
    import sqlite3

    db_path = r'E:\Programowanie\zaRaczke\Back-End\L011_SQLIte\Client_Server_System_SQLite\db_files\test_db_CS_SQLite.db'

    # temp_db_file = config.get('db_path')
    temp_db_file = db_path
    print(f"SQLite: Test database file: {temp_db_file}")
    if not os.path.isabs(temp_db_file):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        temp_db_file = os.path.join(base_dir, temp_db_file)
    temp_db_name = temp_db_file  # Dla SQLite nazwa bazy to plik


    def create_temp_db():
        try:
            if os.path.exists(temp_db_name):
                os.remove(temp_db_name)
            conn = sqlite3.connect(temp_db_name)
            conn.row_factory = sqlite3.Row  # Umożliwia dostęp do wierszy jako słowników
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id integer PRIMARY KEY AUTOINCREMENT,
                    user_name text NOT NULL UNIQUE,
                    permissions text NOT NULL,
                    status text NOT NULL,
                    activation_date date NOT NULL,
                    login_time timestamp
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    message_id integer PRIMARY KEY AUTOINCREMENT,
                    sender_id text,
                    date date NOT NULL,
                    recipient_id text,
                    content text
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                    user_id integer NOT NULL,
                    hashed_password blob NOT NULL,
                    salt blob NOT NULL,
                    PRIMARY KEY (user_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print(f"SQLite: Test database created at {temp_db_name}")
        except Exception as e:
            print(f"An error occurred while creating the SQLite database: {e}")


    def drop_temp_db():
        try:
            if os.path.exists(temp_db_name):
                os.remove(temp_db_name)
                print("SQLite: Test database dropped")
        except Exception as e:
            print(f"An error occurred while dropping the SQLite database: {e}")


    def fill_temp_db():
        try:
            print("SQLite: Test tables filling was started")
            conn = sqlite3.connect(temp_db_name)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            users_data = [
                ("user1", "admin", "active", "2024-02-18"),
                ("user2", "user", "banned", "2024-02-18"),
                ("user3", "user", "active", "2024-02-18"),
                ("user4", "admin", "active", "2024-02-18"),
                ("user5", "user", "banned", "2024-02-18")
            ]
            import bcrypt
            passwords = ["password1", "password2", "password3", "password4", "password5"]
            for idx, user in enumerate(users_data):
                cur.execute("""
                    INSERT INTO users (user_name, permissions, status, activation_date)
                    VALUES (?, ?, ?, ?)
                """, user)
                user_id = cur.lastrowid
                print(f"SQLite: Inserted users: {user_id}")
                # Używamy wartości z listy passwords
                password = passwords[idx].encode('utf-8')
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                cur.execute("""
                    INSERT INTO passwords (user_id, hashed_password, salt)
                    VALUES (?, ?, ?)
                """, (user_id, hashed_password, hashed_password[:29]))
            messages_data = [
                ("user1", "2024-02-18", "user1", "Hello, user2!"),
                ("user2", "2024-02-18", "user2", "Hi there, user3!"),
                ("user1", "2024-02-18", "user3", "Hey user4, how are you?"),
                ("user4", "2024-02-18", "user1", "Greetings, user5!"),
                ("user4", "2024-02-18", "user5", "Welcome, user1!"),
                ("user2", "2024-02-18", "user1", "Hello, user2!"),
                ("user3", "2024-02-18", "user1", "Hello, user2!"),
                ("user5", "2024-02-18", "user1", "Hello, user2!")
            ]
            for message in messages_data:
                cur.execute("""
                    INSERT INTO messages (sender_id, date, recipient_id, content)
                    VALUES (?, ?, ?, ?)
                """, message)
            conn.commit()
            cur.close()
            conn.close()
            print("SQLite: Test tables filling was finished")
        except Exception as e:
            print(f"An error occurred while filling the SQLite database: {e}")
else:
    raise ValueError(f"Unsupported engine: {engine}")
