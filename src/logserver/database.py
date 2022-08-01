from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from config import DB_PATH

SQLALCHEMY_DATABASE_URL = "sqlite:///{}".format(DB_PATH)

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=SingletonThreadPool,
        connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()
except Exception as e:
    print('[Error]', e)
