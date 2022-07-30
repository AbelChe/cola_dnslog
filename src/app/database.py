from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from config import DB_PATH

INSTALL = False

SQLALCHEMY_DATABASE_URL = "sqlite:///{}".format(DB_PATH)

dbfile = os.path.exists(DB_PATH.replace('{HOME}', os.path.expanduser('~')))

if not dbfile:
    print('First use, create dbfile `{}`'.format(DB_PATH.replace('{HOME}', os.path.expanduser('~'))))
    if not os.path.exists(os.path.dirname(DB_PATH.replace('{HOME}', os.path.expanduser('~')))):
        os.makedirs(os.path.dirname(DB_PATH.replace('{HOME}', os.path.expanduser('~'))))
    f = open(DB_PATH.replace('{HOME}', os.path.expanduser('~')), 'w')
    f.close()
    INSTALL = True
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()