import os
from dotenv import load_dotenv

load_dotenv()

SQL_DB_SYSTEM = os.getenv("SQL_DB_SYSTEM")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SERVER = os.getenv("DB_SERVER")
