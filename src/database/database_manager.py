from abc import ABC, abstractmethod

class DatabaseManager(ABC):
    def __init__(self, connection):
        self.connection = connection

    @abstractmethod
    def execute_query(self, query, values=None, return_last_row_id=False):
        pass

    @abstractmethod
    def fetch_one(self, query, values=None):
        pass

    @abstractmethod
    def fetch_all(self, query, values=None):
        pass