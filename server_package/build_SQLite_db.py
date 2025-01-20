import sqlite3
import os


db_path = r'E:\Programowanie\zaRaczke\Back-End\L011_SQLIte\Client_Server_System\db_files\db_CS_SQLite.db'


def create_database():
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
    except sqlite3.Error as e:
        print(f"Error: {e}")
    else:
        print(f"Database created successfully")


def create_table_users():
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                       CREATE TABLE IF NOT EXISTS users (
                          user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_name TEXT NOT NULL,
                          permissions TEXT NOT NULL,
                          status TEXT NOT NULL,
                          activation_date datetime NOT NULL,
                          login_time timestamp
                        )
                        ''')
    except sqlite3.Error as e:
        print(f"Error: {e}")
    else:
        print("Table users created successfully")


def create_table_messages():
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS messages (
                              message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                              sender_id TEXT NOT NULL,
                              date datetime NOT NULL,
                              recipient_id TEXT NOT NULL,
                              content TEXT NOT NULL
                            )
                            ''')
    except sqlite3.Error as e:
        print(f"Error: {e}")
    else:
        print("Table messages created successfully")


def create_table_passwords():
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS passwords (
                              user_id INTEGER PRIMARY KEY,
                              hashed_password BLOB NOT NULL,
                              salt BLOB NOT NULL
                            )
                            ''')
    except sqlite3.Error as e:
        print(f"Error: {e}")
    else:
        print("Table passwords created successfully")


if __name__ == '__main__':
    if os.path.exists(db_path):
        print("Baza danych istnieje.")
    else:
        print("Baza danych nie została znaleziona.")
        create_database()
        create_table_users()
        create_table_messages()
        create_table_passwords()
