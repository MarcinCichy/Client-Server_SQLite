from functools import wraps
import server_package.server_response as server_response
#  Usuwamy: from server_package.connect import connect
from server_package.config import get_db_adapter
from psycopg2 import sql  # Opcjonalnie, jeśli nadal chcesz używać psycopg2.sql.SQL do składania zapytań dynamicznych

def handle_database_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            return server_response.E_DATABASE_ERROR
    return wrapper


class DatabaseSupport:

    def __init__(self):
        """
        W konstruktorze tworzymy adapter bazy danych,
        np. PostgresDBAdapter lub SQLiteDBAdapter, w zależności od configu.
        """
        self.adapter = get_db_adapter()

    @handle_database_errors
    def data_update(self, table, column, user_name, new_value=None):
        # Tworzymy zapytanie. Jeśli korzystasz z psycopg2.sql, możesz zachować sql.SQL(...).
        # Pamiętaj, że w SQLite może być konieczna zamiana %s -> ?
        query = sql.SQL("UPDATE {table} SET {column} = %s WHERE user_name = %s").format(
            table=sql.Identifier(table),
            column=sql.Identifier(column)
        )
        # Wywołujemy execute_query z adaptera. Parametry przekazujemy w krotce (new_value, user_name).
        self.adapter.execute_query(query.as_string(self.adapter.connection), (new_value, user_name))

    @handle_database_errors
    def get_info_about_user(self, user_name):
        """
        Przykład pobierania jednego rekordu (SELECT),
        używamy fetch_one, by otrzymać pojedynczy wynik.
        """
        query = """
            SELECT u.*, p.hashed_password, p.salt
            FROM users u
            JOIN passwords p ON u.user_id = p.user_id
            WHERE u.user_name = %s
        """
        result = self.adapter.fetch_one(query, (user_name,))
        if result:
            # Jeżeli adapter Postgres zwraca dict, a SQLite może zwracać tuple,
            # trzeba się upewnić, że w adapterze SQLite skonwertujesz row do dict,
            # lub dostosujesz tutaj logikę.
            if isinstance(result, dict):
                result_dict = result
            else:
                # W razie czego możesz zrobić mapowanie, np.
                # result_dict = { "user_id": result[0], "user_name": result[1], ... }
                # Ale to wymaga znajomości kolejności kolumn.
                # Dla uproszczenia poniżej zakładamy, że w SQLite też zwracasz dict.
                result_dict = dict(result)

            print(f'RESULT_DICT: {result_dict}')
            return result_dict
        else:
            return None

    @handle_database_errors
    def get_all_users_list(self):
        query = "SELECT user_name, permissions, status FROM users ORDER BY user_id"
        rows = self.adapter.fetch_all(query)
        return rows  # lista krotek lub słowników, zależnie od adaptera

    @handle_database_errors
    def check_if_user_exist(self, user_name):
        query = "SELECT 1 FROM users WHERE user_name = %s"
        row = self.adapter.fetch_one(query, (user_name,))
        return bool(row)  # True jeśli jest, False jeśli brak wyników

    @handle_database_errors
    def inbox_msg_counting(self, recipient_id):
        query = "SELECT COUNT(*) FROM messages WHERE recipient_id = %s"
        row = self.adapter.fetch_one(query, (recipient_id,))
        if row:
            # row może być np. {'count': 5} w Postgres (jeśli DictCursor)
            # lub (5,) w formie krotki.
            # Załóżmy, że zrobimy row[0] gdy jest krotką,
            # lub row['count'] gdy to dict.
            if isinstance(row, dict):
                return list(row.values())[0]
            else:
                return row[0]
        return 0

    @handle_database_errors
    def check_if_user_is_logged_in(self, user_name):
        query = "SELECT login_time FROM users WHERE user_name = %s"
        row = self.adapter.fetch_one(query, (user_name,))
        if row:
            # Podobna uwaga jak wyżej – dict vs tuple
            login_time = row[0] if not isinstance(row, dict) else row.get('login_time')
            return bool(login_time)
        else:
            return False

    @handle_database_errors
    def add_account_to_db(self, new_data, password_data):
        """
        new_data -> krotka (user_name, permissions, status, activation_date)
        password_data -> krotka (hashed_password, salt)
        """
        query_users = """
            INSERT INTO users (user_name, permissions, status, activation_date) 
            VALUES (%s, %s, %s, %s) RETURNING user_id
        """
        # Najpierw pobieramy user_id
        # W adapterze nie mamy wbudowanej metody, która zwraca ID –
        # Można to obsłużyć fetch_one w Postgres (bo tam RETURNING).
        row = self.adapter.fetch_one(query_users, new_data)
        user_id = row[0] if row else None

        if user_id:
            query_passwords = """
                INSERT INTO passwords (user_id, hashed_password, salt) 
                VALUES (%s, %s, %s)
            """
            pass_data_with_id = (user_id,) + password_data
            self.adapter.execute_query(query_passwords, pass_data_with_id)

    @handle_database_errors
    def delete_record_from_db(self, table, data):
        query = sql.SQL("DELETE FROM {table} WHERE user_name = %s").format(
            table=sql.Identifier(table)
        )
        self.adapter.execute_query(query.as_string(self.adapter.connection), (data,))

    @handle_database_errors
    def show_all_messages_inbox(self, username):
        query = "SELECT message_id, sender_id, date FROM messages WHERE recipient_id = %s ORDER BY message_id"
        rows = self.adapter.fetch_all(query, (username,))
        return rows

    @handle_database_errors
    def show_selected_message(self, msg_id):
        query = "SELECT * FROM messages WHERE message_id = %s"
        row = self.adapter.fetch_one(query, (msg_id,))
        if row and isinstance(row, dict):
            print(f'RESULT = {row}')
            return row
        elif row:
            # Tu ewentualnie zamiana tuple -> dict
            # ...
            return row
        else:
            return None

    @handle_database_errors
    def delete_selected_message(self, msg_id):
        query = "DELETE FROM messages WHERE message_id = %s"
        self.adapter.execute_query(query, (msg_id,))

    @handle_database_errors
    def delete_all_user_messages(self, user_to_del):
        query = "DELETE FROM messages WHERE recipient_id = %s"
        self.adapter.execute_query(query, (user_to_del,))

    @handle_database_errors
    def add_new_message_to_db(self, new_data):
        """
        new_data -> np. (sender_id, date, recipient_id, content)
        """
        query = "INSERT INTO messages (sender_id, date, recipient_id, content) VALUES (%s, %s, %s, %s)"
        self.adapter.execute_query(query, new_data)

    @handle_database_errors
    def password_update(self, table, column1, column2, user_id, new_value1=None, new_value2=None):
        # Możesz użyć sql.SQL, by dynamicznie formatować nazwy kolumn/tabel
        query1 = sql.SQL("UPDATE {table} SET {column} = %s WHERE user_id = %s").format(
            table=sql.Identifier(table),
            column=sql.Identifier(column1)
        )
        self.adapter.execute_query(query1.as_string(self.adapter.connection), (new_value1, user_id))

        query2 = sql.SQL("UPDATE {table} SET {column} = %s WHERE user_id = %s").format(
            table=sql.Identifier(table),
            column=sql.Identifier(column2)
        )
        self.adapter.execute_query(query2.as_string(self.adapter.connection), (new_value2, user_id))
