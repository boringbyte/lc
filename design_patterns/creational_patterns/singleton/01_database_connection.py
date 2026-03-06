import threading
import sqlite3


class DatabaseConnection:

    _instance = None
    _lock = threading.Lock()
    _connection = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self, db_name):
        """Initialize connection only once"""
        if self._connection is None:
            print(f"Creating a new database connection to {db_name}")
            self._connection = sqlite3.connect(db_name, check_same_thread=False)
        else:
            print(f"Using existing database connection to {db_name}")
        return self._connection

    def execute_query(self, query):
        if self._connection is None:
            raise Exception("Database not connected. Call connect() first.")

        cursor = self._connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            print("Database connection closed")


if __name__ == '__main__':
    db1 = DatabaseConnection()
    db1.connect("myapp.db")

    db2 = DatabaseConnection()
    db2.connect("myapp.db")
    print(db1 is db2)

    results = db1.execute_query("SELECT name FROM sqlite_master WHERE type='table';")
    for result in results:
        print(result[0])

    db2.close()
