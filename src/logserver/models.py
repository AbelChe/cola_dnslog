from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    roles = Column(String(255))
    hashed_password = Column(String(255))
    token = Column(String(255), unique=True)
    logid = Column(String(255), unique=True)
    dingtalk_robot_token = Column(String(255))
    bark_url = Column(String(255), default='https://api.day.app/XXXXXXXXXXXXXXXXXXXX/')
    is_active = Column(Boolean, default=True)
    dingtalk_flag = Column(Boolean, default=False)
    bark_flag = Column(Boolean, default=False)
    register_time = Column(DateTime, nullable=False, server_default=func.now())
    last_logintime = Column(DateTime, nullable=True, onupdate=func.now())

    dnslog_item = relationship('Dnslog', backref='user')
    httplog_item = relationship('Httplog', backref='user')
    ldaplog_item = relationship('Ldaplog', backref='user')
    rmilog_item = relationship('Rmilog', backref='user')

class Dnslog(Base):
    __tablename__ = 'dnslog'

    id = Column(Integer, primary_key=True, index=True)
    record = Column(Text())
    ip_from = Column(String(255))
    record_time = Column(DateTime, nullable=False, server_default=func.now())
    owner_id = Column(Integer, ForeignKey('user.id'))

class Httplog(Base):
    __tablename__ = 'httplog'

    id = Column(Integer, primary_key=True, index=True)
    headers = Column(Text())
    request_method = Column(String(255))
    content_length = Column(Integer, nullable=False, default=-1)
    path = Column(Text())
    body_data = Column(Text(), nullable=True)
    ip_from = Column(String(255))
    useragent = Column(Text())
    record_time = Column(DateTime, nullable=False, server_default=func.now())
    owner_id = Column(Integer, ForeignKey('user.id'))

class Ldaplog(Base):
    __tablename__ = 'ldaplog'

    id = Column(Integer, primary_key=True, index=True)
    pathname = Column(Text())
    ip_from = Column(String(255))
    record_time = Column(DateTime, nullable=False, server_default=func.now())
    owner_id = Column(Integer, ForeignKey('user.id'))

class Rmilog(Base):
    __tablename__ = 'rmilog'

    id = Column(Integer, primary_key=True, index=True)
    objectname = Column(Text())
    rmi_client_ip = Column(String(255))
    ip_from = Column(String(255))
    record_time = Column(DateTime, nullable=False, server_default=func.now())
    owner_id = Column(Integer, ForeignKey('user.id'))
