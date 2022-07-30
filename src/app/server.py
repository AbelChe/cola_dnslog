#/usr/bin/env python3

import os
import random
import string
import sys

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import sessionmaker
from libs.auth import password_hash

from config import HOST, PORT
from database import INSTALL, Base, engine
from models import Dnslog, Httplog, User
from routers import auth, dnslog, httplog, ldaplog, rmilog

sys.path.append(os.path.join(os.path.dirname(__file__)))

root_router = APIRouter(
    prefix="/api",
    tags=["api"]
)

app = FastAPI()

root_router.include_router(dnslog.router)
root_router.include_router(httplog.router)
root_router.include_router(ldaplog.router)
root_router.include_router(rmilog.router)
root_router.include_router(auth.router)

app.include_router(root_router)

try:
    for i in [User, Dnslog, Httplog]:
        if not engine.dialect.has_table(engine.connect(), i.__tablename__):
            Base.metadata.create_all(engine)
            print('[+] Table `{}` create success'.format(i.__tablename__))
        else:
            print('[+] Table `{}` has been created, go on'.format(i.__tablename__))
except Exception as e:
    print('[-]', e)

if INSTALL:
    Session_class = sessionmaker(bind=engine)
    Session = Session_class()
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(24))
    roles = 'admin'
    hashpwd = password_hash(password)
    token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32)).lower()
    logid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3)).lower()
    sql_obj = User(name='admin', roles=roles, hashed_password=hashpwd, token=token, logid=logid)
    Session.add(sql_obj)
    Session.commit()
    print('[+] -------------Add init user-------------')
    print('[+] username: admin')
    print('[+] password: {}'.format(password))
    print('[+] token: {}'.format(token))
    print('[+] logid: {}'.format(logid))
    print('[+] ---------------------------------------')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

@app.get("/")
async def root():
    return {"status": "Server OK..."}

if __name__ == '__main__':
    uvicorn.run(
        'server:app',
        port=PORT,
        host=HOST,
        reload=True
    )
