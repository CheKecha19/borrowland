# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL

engine = create_engine(DB_URL, echo=False, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})
SessionLocal = sessionmaker(bind=engine)
