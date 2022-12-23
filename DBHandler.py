import psycopg2
import unified_exceptions as ue
from dotenv import load_dotenv
import os
import sys


# Load .env file with credentials

load_dotenv() 

######################## Set up logging system ##########################

filename="Logs/logs.txt"
header = sys.argv[0].split("/")[-1]
exception_handler = ue.UnifiedExceptions(filename)


########################## DB handling classe ############################

class handler:
    def __init__(self, db_name: str, *schema: str) -> None:

        """
        Try to connect to database with db_name. If it exists, we have a successfull connection. 
        If it does not exist, the programm connects to the default postgres DB and creates a DB with name db_name
        After the creation of the DB, it connects to it and creates the specified tables

        """

        try:
            self.connection = self.create_connection(db_name=db_name, db_user=os.getenv('USERNAME'), db_password=os.getenv('PASSWORD'), db_host="127.0.0.1", db_port="5432")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        
        except Exception as e:
            try:
                self.create_db(db_name)
                self.connection = self.create_connection(db_name=db_name, db_user=os.getenv('USERNAME'), db_password=os.getenv('PASSWORD'), db_host="127.0.0.1", db_port="5432")
                self.cursor = self.connection.cursor()
            
            except Exception as e:
                exception_handler.error(f"{header}\tException occurred {e}")
        
        try:
            for query in schema:
                exception_handler.debug(f"{header}\tIn for loop from "+str(schema)+ " creating "+str(query))
                self.create_schema(query)
        
        except psycopg2.errors.DuplicateObject as e:
            exception_handler.error(f"{header}\tException occurred {e}")

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
        
        exception_handler.info(f"{header}\tConnection to PostgreSQL DB '{db_name}' successful")

        return connection
    
    @exception_handler.handle
    def create_db(self, db_name :str) -> None:
        self.connection = self.create_connection(db_name="postgres", db_user="postgres", db_password="minda", db_host="127.0.0.1", db_port="5432")
        self.connection.autocommit = True
        #self.connection.cursor().execute(str("CREATE DATABASE "+db_name))
        self.execute_query(str("CREATE DATABASE "+db_name))
        exception_handler.info(f"{header}\tDatabase created successfully")
    
    @exception_handler.handle
    def execute_query(self, query: str) -> None:
        self.connection.cursor().execute(query)
        exception_handler.info(f"{header}\tQuery executed successfully")
    
    @exception_handler.handle
    def create_schema(self, schema: str) -> None:
        with open(schema, encoding = 'utf-8') as f:
            exception_handler.debug(f"{header}\tCreating {f.read()}")
            self.cursor.execute(f.read())
            self.connection.commit()
    
    @exception_handler.handle
    def insert(self, table_name, table_schema, data):
        exception_handler.debug(f"{header}\tExecuting: INSERT INTO {table_name} {table_schema} VALUES {tuple(data)}")
        self.cursor.execute(f"INSERT INTO {table_name} {table_schema} VALUES {tuple(data)}")
        self.connection.commit()

    @exception_handler.handle
    def get(self, table_name, get_by="", value=None, set_limit=False, limit=10):
        exception_handler.debug(f"{header}\tExecuting: SELECT * FROM {table_name}" + str(f" WHERE {get_by} = '{value}'" if len(get_by) else "") + str(f" LIMIT {limit}" if set_limit else ""))
        self.cursor.execute(f"SELECT * FROM {table_name}" + str(f" WHERE {get_by} = '{value}'" if len(get_by) else "") + str(f" LIMIT {limit}" if set_limit else ""))
        return self.cursor.fetchall()
