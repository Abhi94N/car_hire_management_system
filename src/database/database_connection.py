from abc import ABC, abstractmethod

class DatabaseConnection(ABC):
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conn = self.create_db_connection()

    @abstractmethod
    def create_db_connection(self):
        pass

    def disconnect(self):
        if self.conn:
            self.conn.close()