import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database:

    def __init__(self):
        self.config = DB_CONFIG
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    def execute_query(self, query, params=None, commit=False):
        connection = self.connect()
        if not connection:
            raise Exception("Could not connect to database")
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if commit:
                connection.commit()
            return cursor
        except Error as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()

    def fetch_all(self, query, params=None):
        cursor = None
        connection = None
        try:
            connection = self.connect()
            if not connection:
                return []
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def fetch_one(self, query, params=None):
        cursor = None
        connection = None
        try:
            connection = self.connect()
            if not connection:
                return None
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching record: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
