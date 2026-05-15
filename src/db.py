from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
SERVER = os.getenv("DB_SERVER")
PORT = os.getenv("DB_PORT")
DB = os.getenv("DB")

DATABASE_URL = f"mysql+pymysql://{USER}:{PASS}@{SERVER}:{PORT}/{DB}"

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()