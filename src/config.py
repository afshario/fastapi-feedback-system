import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("USER")
PASS = os.getenv("PASS")
SERVER = os.getenv("SERVER")
PORT = os.getenv("PORT")
DB = os.getenv("DB")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
# REDIS_PASS = os.getenv("REDIS_PASS")
# REDIS_HOST = os.getenv("REDIS_HOST")