import mysql.connector
from .database_manager import DatabaseManager

class MySQLDatabaseManager(DatabaseManager):
    def __init__(self, connection):
        self.connection = connection

    def execute_query(self, query, values=None, return_last_row_id=False):
        try:
            cursor = self.connection.conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)

            if return_last_row_id and query.strip().lower().startswith("insert"):
                lastrowid = cursor.lastrowid
            else:
                lastrowid = None

            self.connection.conn.commit()
            cursor.close()

            return True, lastrowid

        except mysql.connector.Error as e:
            error_code = e.errno
            if error_code == 1062:
                return False, "Duplicate entry error: This record already exists."
            else:
                print(f"Error executing query: {e}")
                self.connection.conn.rollback()
                return False, str(e)

    def fetch_one(self, query, values=None):
        try:
            cursor = self.connection.conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result

        except Exception as e:
            return str(e)