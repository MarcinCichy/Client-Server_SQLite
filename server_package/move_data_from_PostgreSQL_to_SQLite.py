import psycopg2
import sqlite3

# Ścieżka do istniejącej bazy SQLite (plik musi już istnieć i zawierać odpowiednie tabele)
db_path = r'E:\Programowanie\zaRaczke\Back-End\L003\Client_Server_System\db_files\db_CS_SQLite.db'

# Ustawienia połączenia z PostgreSQL (dostosuj do swoich danych)
pg_config = {
    'dbname': 'db_CS',
    'user': 'postgres',
    'password': 'MC',
    'host': '127.0.0.1',  # np. 'localhost'
    'port': 5432
}


def migrate_users(pg_cursor, sqlite_cursor):
    """Migracja danych z tabeli users"""
    pg_cursor.execute("SELECT user_id, user_name, permissions, status, activation_date, login_time FROM users")
    rows = pg_cursor.fetchall()

    insert_query = """
        INSERT INTO users (user_id, user_name, permissions, status, activation_date, login_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    for row in rows:
        try:
            sqlite_cursor.execute(insert_query, row)
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError przy migracji rekordu users {row}: {e}")


def migrate_messages(pg_cursor, sqlite_cursor):
    """Migracja danych z tabeli messages"""
    pg_cursor.execute("SELECT message_id, sender_id, date, recipient_id, content FROM messages")
    rows = pg_cursor.fetchall()

    insert_query = """
        INSERT INTO messages (message_id, sender_id, date, recipient_id, content)
        VALUES (?, ?, ?, ?, ?)
    """
    for row in rows:
        try:
            sqlite_cursor.execute(insert_query, row)
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError przy migracji rekordu messages {row}: {e}")


def migrate_passwords(pg_cursor, sqlite_cursor):
    """Migracja danych z tabeli passwords"""
    pg_cursor.execute("SELECT user_id, hashed_password, salt FROM passwords")
    rows = pg_cursor.fetchall()

    insert_query = """
        INSERT INTO passwords (user_id, hashed_password, salt)
        VALUES (?, ?, ?)
    """
    for row in rows:
        try:
            sqlite_cursor.execute(insert_query, row)
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError przy migracji rekordu passwords {row}: {e}")


def migrate_data():
    # Połączenie z PostgreSQL
    try:
        pg_conn = psycopg2.connect(**pg_config)
        pg_cursor = pg_conn.cursor()
    except Exception as e:
        print("Błąd połączenia z PostgreSQL:", e)
        return

    # Połączenie z już istniejącą bazą SQLite
    try:
        sqlite_conn = sqlite3.connect(db_path)
        sqlite_cursor = sqlite_conn.cursor()
    except Exception as e:
        print("Błąd połączenia z SQLite:", e)
        pg_cursor.close()
        pg_conn.close()
        return

    try:
        # Opcjonalnie: wyczyszczenie tabel w SQLite przed migracją
        sqlite_cursor.execute("DELETE FROM users")
        sqlite_cursor.execute("DELETE FROM messages")
        sqlite_cursor.execute("DELETE FROM passwords")
        sqlite_conn.commit()

        # Migracja kolejno użytkowników, wiadomości i haseł
        migrate_users(pg_cursor, sqlite_cursor)
        migrate_messages(pg_cursor, sqlite_cursor)
        migrate_passwords(pg_cursor, sqlite_cursor)

        sqlite_conn.commit()
        print("Migracja danych zakończona pomyślnie.")

    except Exception as e:
        print("Błąd podczas migracji:", e)
    finally:
        # Zamknięcie połączeń
        pg_cursor.close()
        pg_conn.close()
        sqlite_conn.close()


if __name__ == '__main__':
    migrate_data()
