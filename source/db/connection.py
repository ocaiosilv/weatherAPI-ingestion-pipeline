from dotenv import load_dotenv
from sqlalchemy import create_engine
import os


def get_credentials():
    load_dotenv()

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    return db_host, db_port, db_name, db_user, db_password

#Follow the official docs https://docs.sqlalchemy.org/en/21/core/engines.html for DBMS change
def db_connect():
    db_host, db_port, db_name, db_user, db_password = get_credentials()
    engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    return engine