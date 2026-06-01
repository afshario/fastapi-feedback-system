import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
SERVER = os.getenv("DB_SERVER")
PORT = os.getenv("DB_PORT")
DB = os.getenv("DB")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")