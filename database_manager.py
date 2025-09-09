# database_manager.py (Updated with auto-reconnect logic for PyMySQL)

import pymysql
from pymysql import Error

class DatabaseManager:
    """
    A class to manage all database connections and operations.
    This version includes logic to handle database timeouts by reconnecting.
    """
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establishes a new connection to the database."""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True  # Simplifies transactions for this app
            )
            print("Successfully connected/reconnected to the database.")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None

    def _ensure_connection(self):
        """
        Checks if the database connection is alive.
        If not, it attempts to reconnect.
        """
        if self.connection is None:
            print("No existing connection. Connecting...")
            self.connect()
            return

        try:
            # ping() is the standard way to check a connection and reconnect if lost
            self.connection.ping(reconnect=True)
        except Error as e:
            print(f"Database connection lost. Attempting to reconnect... Error: {e}")
            self.connect()

    def disconnect(self):
        """Closes the database connection."""
        if self.connection and self.connection.open:
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        """Executes a query after ensuring the connection is active."""
        self._ensure_connection()
        if not (self.connection and self.connection.open):
            print("Could not establish a database connection.")
            return False
        
        try:
            # 'with' statement ensures the cursor is closed properly
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
            # self.connection.commit() is not needed due to autocommit=True
            print("Query executed successfully.")
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            # In case of a major error, try to reconnect for the next attempt
            self.connect() 
            return False

    def fetch_all(self, query, params=None):
        """Fetches all results after ensuring the connection is active."""
        self._ensure_connection()
        if not (self.connection and self.connection.open):
            print("Could not establish a database connection.")
            return []
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Error fetching data: {e}")
            # In case of a major error, try to reconnect for the next attempt
            self.connect()
            return []
