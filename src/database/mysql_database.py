import os
import mysql.connector

class MySQLDatabase:
    def __init__(self):
        self.conn = self.create_db_connection()

    def create_db_connection(self):
        mysql_config = {
            'host': os.environ.get('MYSQL_HOST'),
            'user': os.environ.get('MYSQL_USER'),
            'port': os.environ.get('MYSQL_PORT'),
            'password': os.environ.get('MYSQL_PASSWORD'),
            'database': os.environ.get('MYSQL_DB'),
        }

        try:
            conn = mysql.connector.connect(**mysql_config)
            print("MySQL connection successful!")
            return conn
        except mysql.connector.Error as err:
            print(f"MySQL connection error: {err}")
    
    def execute_query(self, query, values=None, return_last_row_id=False):
        try:
            cursor = self.conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)

            if return_last_row_id and query.strip().lower().startswith("insert"):
                lastrowid = cursor.lastrowid
            else:
                lastrowid = None

            self.conn.commit()
            cursor.close()

            return True, lastrowid
        except mysql.connector.Error as e:
            error_code = e.errno
            if error_code == 1062:
                return False, "Duplicate entry error: This record already exists."
            else:
                print(f"Error executing query: {e}")
                self.conn.rollback()
                return False, str(e)

    def fetch_one(self, query, values=None):
        try:
            cursor = self.conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            return str(e)