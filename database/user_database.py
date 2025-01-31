import sqlite3
import hashlib

class UserDatabaseSingleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_singleton_instance'):
            # first call
            cls._singleton_instance = super().__new__(cls)
        # already created
        return cls._singleton_instance
    
    def __init__(self, db_name='user_database.db'):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.db_name = db_name
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.create_table()
            self.close_connection() # close the connection after creating the table

    def create_table(self):
        '''Create a table in the database'''
        table_name = 'users'
        column_1 = 'id'
        column_2 = 'username'
        column_3 = 'password'
        sql_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name}(
            {column_1} INTEGER PRIMARY KEY AUTOINCREMENT, 
            {column_2} TEXT NOT NULL UNIQUE,
            {column_3} TEXT NOT NULL
        )"""
        self.cursor.execute(sql_query)
        self.conn.commit()
        
    def add_user(self, username: str, password: str) -> bool:
        '''Insert a new user into the database: 
        Return True if the user was inserted in the queue, 
        False otherwise'''
        self.open_connection()
        try:
            assert isinstance(username, str) and isinstance(password, str), 'username and password must be strings'
            def write():
                sql_query = """
                INSERT INTO users(username, password) VALUES (?, ?)
                """
                return sql_query        
            self.cursor.execute(write(), (username, compute_hash(password)))
            self.conn.commit()
            assert self.cursor.rowcount == 1, 'User not added'
            self.close_connection()
            return True
        except(Exception) as e:
            print(e)
            print('User not added')
            return False

    def login_user(self, username: str, password: str) -> bool:
        '''log in if the user and password are in the database:
        Return True if that so,
        False otherwise'''
        self.open_connection()
        try:
            assert isinstance(username, str) and isinstance(password, str), 'username and password must be strings'
            def read():
                sql_query = """
                SELECT 1 FROM users
                WHERE username = ? AND password = ?
                """
                return sql_query
            self.cursor.execute(read(), (username, compute_hash(password))) 
            self.conn.commit()
            result = self.cursor.fetchone()
            self.close_connection()
            return result is not None
        except(Exception) as e:
            print(e)
            return False
        
    def delete_user(self, username: str, password: str) -> bool:
        '''Delete a user from the database:
        Return True if the user was deleted,
        False otherwise'''
        self.open_connection()
        try:
            assert isinstance(username, str), 'username must be a string'
            def delete():
                sql_query = """
                DELETE FROM users
                WHERE username = ? and password = ?
                """
                return sql_query
            self.cursor.execute(delete(), (username,password))
            self.conn.commit()
            self.close_connection()
            return True
        except(Exception) as e:
            print(e)
            return False
    
    def format_database(self):
        '''Delete all the data from the database'''
        self.open_connection()
        try:
            def delete_all():
                sql_query = """
                DELETE FROM users
                """
                return sql_query
            self.cursor.execute(delete_all())
            self.conn.commit()
            self.close_connection()
            return True
        except(Exception) as e:
            print(e)
            return False
        
    def open_connection(self):
        '''Open the database connection'''
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        
    def close_connection(self):
        '''Close the database connection'''
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

def compute_hash(password: str) -> str:
    '''Compute the hash of a password'''
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    db = UserDatabaseSingleton()
    if db.add_user('giovanni', 'admin'):
        print('User added!')
    if db.login_user('giovanni', 'admin'):
        print('Logged in!')