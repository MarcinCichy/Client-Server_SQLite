from functools import wraps
import server_package.server_response as server_response
from server_package.config import get_db_adapter
from psycopg2 import sql


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
        self.adapter = get_db_adapter()

    # @handle_database_errors
    # def data_update(self, table, column, user_name, new_value=None):
    #     query = sql.SQL("UPDATE {table} SET {column} = %s WHERE user_name = %s").format(
    #         table=sql.Identifier(table),
    #         column=sql.Identifier(column)
    #     )
    #     self.adapter.execute_query(query.as_string(self.adapter.connection), (new_value, user_name))

    @handle_database_errors
    def data_update(self, table, column, user_name, new_value=None):
        # Jeśli adapter to SQLite, budujemy zapytanie przy użyciu f-stringa i placeholderów '?'.
        if self.adapter.__class__.__name__ == "SQLiteDBAdapter":
            query = f"UPDATE {table} SET {column} = ? WHERE user_name = ?"
            self.adapter.execute_query(query, (new_value, user_name))
        else:
            # Dla PostgreSQL używamy psycopg2.sql, gdzie placeholdery to %s.
            query = sql.SQL("UPDATE {table} SET {column} = %s WHERE user_name = %s").format(
                table=sql.Identifier(table),
                column=sql.Identifier(column)
            )
            self.adapter.execute_query(query.as_string(self.adapter.connection), (new_value, user_name))

    @handle_database_errors
    def get_info_about_user(self, user_name):
        query = """
            SELECT u.*, p.hashed_password, p.salt
            FROM users u
            JOIN passwords p ON u.user_id = p.user_id
            WHERE u.user_name = %s
        """
        result = self.adapter.fetch_one(query, (user_name,))
        if result:
            # print(f'RESULT_DICT: {result}')
            return result
        else:
            return None

    @handle_database_errors
    def get_all_users_list(self):
        query = "SELECT user_name, permissions, status FROM users ORDER BY user_id"
        rows = self.adapter.fetch_all(query)
        return rows

    @handle_database_errors
    def check_if_user_exist(self, user_name):
        query = "SELECT 1 FROM users WHERE user_name = %s"
        row = self.adapter.fetch_one(query, (user_name,))
        return bool(row)

    @handle_database_errors
    def inbox_msg_counting(self, recipient_id):
        query = "SELECT COUNT(*) as cnt FROM messages WHERE recipient_id = %s"
        row = self.adapter.fetch_one(query, (recipient_id,))
        if row:
            return row['cnt']  # bo z adaptera mamy np. {'cnt': 5}
        return 0

    @handle_database_errors
    def check_if_user_is_logged_in(self, user_name):
        query = "SELECT login_time FROM users WHERE user_name = %s"
        row = self.adapter.fetch_one(query, (user_name,))
        if row and row.get('login_time'):
            return True
        else:
            return False

    @handle_database_errors
    def add_account_to_db(self, new_data, password_data):
        query_users = """
            INSERT INTO users (user_name, permissions, status, activation_date)
            VALUES (%s, %s, %s, %s)
            RETURNING user_id
        """
        row = self.adapter.fetch_one(query_users, new_data)
        user_id = row['user_id'] if row else None
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
        return row if row else None

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
        query = "INSERT INTO messages (sender_id, date, recipient_id, content) VALUES (%s, %s, %s, %s)"
        self.adapter.execute_query(query, new_data)

    # @handle_database_errors
    # def password_update(self, table, column1, column2, user_id, new_value1=None, new_value2=None):
    #     query1 = sql.SQL("UPDATE {table} SET {column} = %s WHERE user_id = %s").format(
    #         table=sql.Identifier(table),
    #         column=sql.Identifier(column1)
    #     )
    #     self.adapter.execute_query(query1.as_string(self.adapter.connection), (new_value1, user_id))
    #
    #     query2 = sql.SQL("UPDATE {table} SET {column} = %s WHERE user_id = %s").format(
    #         table=sql.Identifier(table),
    #         column=sql.Identifier(column2)
    #     )
    #     self.adapter.execute_query(query2.as_string(self.adapter.connection), (new_value2, user_id))

    @handle_database_errors
    def password_update(self, table, column1, column2, user_id, new_value1=None, new_value2=None):
        if self.adapter.__class__.__name__ == "SQLiteDBAdapter":
            # Dla SQLite budujemy zapytania przy użyciu f-stringa i placeholderów '?'
            query1 = f"UPDATE {table} SET {column1} = ? WHERE user_id = ?"
            self.adapter.execute_query(query1, (new_value1, user_id))

            query2 = f"UPDATE {table} SET {column2} = ? WHERE user_id = ?"
            self.adapter.execute_query(query2, (new_value2, user_id))
        else:
            # Dla PostgreSQL używamy psycopg2.sql
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
