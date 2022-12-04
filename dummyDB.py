import psycopg2
from psycopg2 import OperationalError
import logging
import unified_exceptions as ue

exception_handler = ue.UnifiedExceptions("logs.txt")

logging.basicConfig(level=logging.DEBUG, filename="DB_logs.txt", format='[%(asctime)s] %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class handler:
    def __init__(self, db_name: str, *tables: str) -> None:
        """
        Try to connect to database with db_name. If it exists, we have a successfull connection. 
        If it does not exist, the programm connects to the default postgres db and creates a bd with name db_name
        After the creation of the db, it connects to it and creates the specified tables

        """

        try:
            self.connection = self.create_connection(db_name=db_name, db_user="postgres", db_password="minda", db_host="127.0.0.1", db_port="5432")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except Exception as e:
            try:
                self.create_db(db_name)
                self.connection = self.create_connection(db_name=db_name, db_user="postgres", db_password="minda", db_host="127.0.0.1", db_port="5432")
                self.cursor = self.connection.cursor()
            except Exception as e:
                logging.error("Exception occurred", exc_info=True)
        
        for table in tables:
            self.create_tables(self.connection, table)        

    @exception_handler.handle
    def create_connection(self, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str) -> psycopg2.connect:
        connection = None
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        
        logging.info("Connection to PostgreSQL DB '{}' successful".format(db_name))

        return connection
    
    @exception_handler.handle
    def create_db(self, db_name :str) -> None:
        self.connection = self.create_connection(db_name="postgres", db_user="postgres", db_password="minda", db_host="127.0.0.1", db_port="5432")
        self.connection.autocommit = True
        self.connection.cursor().execute(str("CREATE DATABASE "+db_name))
        logging.info("Database created successfully")
    
    @exception_handler.handle
    def execute_query(self, query: str) -> None:
        self.cursor.execute(query)
        logging.info("Query executed successfully")
    
    @exception_handler.handle
    def create_table(self, connection: psycopg2.connect, table: str) -> None:
        with open(table, encoding = 'utf-8') as f:
            self.execute_query(connection, f.read())

    
    @exception_handler.handle
    def insert(self, table_name, table_schema, *data):
        self.execute_query(f"INSERT INTO {table_name} {table_schema} VALUES {(*list, )}")
