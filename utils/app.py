import cx_Oracle
import json
import logging
from django.conf import settings


logger = logging.getLogger(__name__)

class OracleDB:
    def __init__(self):
        self.dsn = cx_Oracle.makedsn(settings.DATABASES['validation']['HOST'], 
                                     settings.DATABASES['validation']['PORT'], 
                                     service_name=settings.DATABASES['validation']['NAME'])
        self.user = settings.DATABASES['validation']['USER']
        self.password = settings.DATABASES['validation']['PASSWORD']
        self.connection = None

    def connect(self):
        try:
            self.connection = cx_Oracle.connect(user=self.user, password=self.password, dsn=self.dsn)
            logger.info("Connected to commissions db successfully")
            print("Connected to commissions db successfully")
        except cx_Oracle.Error as e:
            logger.error("Error connecting to Oracle DB commissions db")
            print("Error connecting to Oracle DB commissions db")
            self.connection = None

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None


    def callProcedure(self,procedure_name):
        if not self.connection:
           
            return None

        cursor = self.connection.cursor()

        try:
            cursor.callproc(procedure_name)
            print(f"Procedure executed successfully. {procedure_name}")
        except cx_Oracle.DatabaseError as e:
            print(f"Error executing procedure: {e} in {procedure_name}")

        # Close the cursor and connection
        cursor.close()
        


    def execute_query(self, query, params=None):
        if not self.connection:
           
            return None

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or {})
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            result = [dict(zip(columns, row)) for row in rows]
            cursor.close()
            return json.dumps(result, default=str)

        except cx_Oracle.DatabaseError as e:
            error, = e.args
            self.handle_database_error(error)
            cursor.close()
            return None
        
    def execute_stored_procedure(self, procedure_name):
        if not self.connection:
            
            return False

        cursor = self.connection.cursor()
        try:
            cursor.execute(f"CALL {procedure_name}()")
            self.connection.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            self.handle_database_error(error)
            return False
        except Exception as e:
            logger.error(f"Unexpected error during procedure execution: {str(e)}")
            return False
        finally:
            cursor.close()
    def insert_data(self, query, params=None):
        if not self.connection:
            
            return False

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or {})
            self.connection.commit()
            cursor.close()
            return True
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            self.handle_database_error(error, params)
            cursor.close()
            return False

    def handle_database_error(self, error, params=None):
        if error.code == 1861:
            logger.error("Database error: Invalid date format.")
        elif error.code == 942:
            logger.error("Database error: Table or view does not exist.")
        elif error.code == 12899:
            logger.error("Database error: Value too large for column.")
        elif error.code == 1400:
            logger.error("Database error: Cannot insert NULL into column.")
        else:
            if error.code == 6502 or error.code == 1722:
                logger.error("Database error: Numeric or value error.")
                if params:
                    logger.error("Data type mismatch detected.")
            logger.error("Database error occurred.")


