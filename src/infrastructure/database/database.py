# infrastructure/database/database.py
import pyodbc

class Database:

    # Connect to database
    def __init__(self, connection_string):

        try:
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
        except pyodbc.Error as e:
            print(f"Connection error: {e}")
            raise
    
    # Execute a sql query
    def execute(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
        except pyodbc.Error as e:
            self.connection.rollback()
            print(f"Error during query execution: {e}")
            raise

    # Execute a sql query and return all rows
    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Error getting rows: {e}")
            raise

    def fetch_one(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            print(f"Error getting row: {e}")
            raise

    # Close database connection
    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except pyodbc.Error as e:
            print(f"Error clossing the connection: {e}")
            raise