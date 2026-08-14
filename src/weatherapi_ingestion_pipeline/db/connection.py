import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError
import time


def get_credentials(): 

    server = os.getenv('AZURE_SQL_SERVER')
    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER=tcp:{os.getenv('AZURE_SQL_SERVER')}.database.windows.net,1433;"
        f"DATABASE={os.getenv('AZURE_SQL_DATABASE')};"
        f"UID={os.getenv('AZURE_SQL_USER')};"
        f"PWD={os.getenv('AZURE_SQL_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Timeout=30;"
    )
    return connection_string

def db_connect():
    connection_string = get_credentials()
    engine = create_engine(
        "mssql+pyodbc:///?odbc_connect=" + quote_plus(connection_string)
    )
    return engine

def db_connect_retry():
    engine = db_connect() 
    for attempt in range(1, 6):
        try:
            with engine.connect() as conn:
                return engine
                
        except DBAPIError as e:
            if '40613' in str(e) or 'HY000' in str(e):
                time.sleep(15)
            else:
                raise e
                
    raise Exception("Timeout")



