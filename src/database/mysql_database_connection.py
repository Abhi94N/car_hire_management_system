import mysql.connector
from .database_connection import DatabaseConnection

class MySQLDatabaseConnection(DatabaseConnection):
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conn = self.create_db_connection()

    def create_db_connection(self):

        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            print("MySQL connection successful!")
            return self.conn
        except mysql.connector.Error as err:
            print(f"MySQL connection error: {err}")
            return False

    def disconnect(self):
        if self.conn:
            self.conn.close()