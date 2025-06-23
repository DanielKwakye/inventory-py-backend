# Singleton Pattern for Database Connection
#The Singleton Pattern is a Creational design pattern that ensures a class has only one instance
#and provides a global point of access to that instance.
import sqlite3

class DatabaseConnection:
    _instance = None  # Singleton instance

    def __new__(cls, db_name="database.db"):
        if cls._instance is None:
            print("Creating a new database connection...")
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._db_name = db_name
            cls._instance._connection = sqlite3.connect(db_name)
        return cls._instance

    def get_connection(self):
        return self._connection

    def close_connection(self):
        if self._connection:
            print("Closing the database connection...")
            self._connection.close()
            DatabaseConnection._instance = None  # Reset the singleton