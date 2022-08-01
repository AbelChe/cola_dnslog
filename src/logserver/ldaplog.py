import datetime
import os
import re
import socket
import threading

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from config import LDAP_HOST, LDAP_PORT, TEMPLATES_PATH
from database import engine
from models import Ldaplog, User
from utils import bark_message_sender, dingtalk_robot_message_sender

LDAP_FINGERPRINT = b'\x30\x0c\x02\x01\x01\x60\x07\x02\x01\x03\x04\x00\x80\x00'
LDAP_RETURN_1 = b'\x30\x0c\x02\x01\x01\x61\x07\x0a\x01\x00\x04\x00\x04\x00'

# Load dingtalk template
dingtalk_robot_message_template_file = open(os.path.join(TEMPLATES_PATH, 'dingtalk', 'ldaplog.md'))
dingtalk_robot_message_template = dingtalk_robot_message_template_file.read()
dingtalk_robot_message_template_file.close()

bark_robot_message_template_file = open(os.path.join(TEMPLATES_PATH, 'bark', 'ldaplog.txt'))
bark_robot_message_template = bark_robot_message_template_file.read()
bark_robot_message_template_file.close()

Session_class = sessionmaker(bind=engine)
Session = Session_class()

def link_handler(link, client):
    print("[R] Receive from {}:{}".format(client[0], client[1]))
    while True:
        client_data1 = link.recv(1024)
        if client_data1 == LDAP_FINGERPRINT:
            # print(' [+] Received ldap package 1')
            link.send(LDAP_RETURN_1)
            client_data2 = link.recv(1024)
            # check the second package
            if len(client_data2) == client_data2[1]+2:
                # print(' [+] Received ldap package 2')
                path_length = client_data2[8]
                path = client_data2[9:9+path_length].decode('utf8')
                print(' [{}] Path: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), path))
                logid = path[-3::]
                try:
                    if len(logid) != 3:
                        break
                    user_selectobj = Session.query(User).filter_by(logid=logid)
                    user_selectdata = user_selectobj.first()
                    if user_selectdata:
                        sql_obj = Ldaplog(pathname=path, ip_from=client[0], record_time=func.now(), owner_id=user_selectdata.id)
                        Session.add(sql_obj)
                        Session.commit()
                        print('[+ SQL] pathname--->{} \t type--->{} \t ip--->{}'.format(path, 'LDAP', client[0]))
                        message_sender(sql_obj)
                except Exception as e:
                    Session.rollback()
                    print('[SQL ERROR] ' + path + ' ' + str(e))
                    f = open('sqlerror.txt', 'a')
                    f.write('[+ SQL] pathname--->{} \t type--->{} \t ip--->{}'.format(path, 'LDAP', client[0]))
                    f.write('\n')
                    f.write(str(e))
                    f.write('\n----------------------------------------')
                    f.close()
                finally:
                    Session.close()
                break
            break
        break
    link.close()

def message_sender(data: Ldaplog):
    userobj = Session.query(User).filter_by(id=data.owner_id).first()
    DingtalkFlag = userobj.dingtalk_flag
    BarkFlag = userobj.bark_flag
    if DingtalkFlag:
        field_list = re.findall(r'\$\{.*?\}\$', dingtalk_robot_message_template)
        message = dingtalk_robot_message_template
        for i in field_list:
            message = message.replace(i, str(getattr(data, i.replace('${', '').replace('}$', ''))))
        dingtalk_robot_message_sender(userobj.dingtalk_robot_token, 'LDAP请求 '+data.pathname, message)
    if BarkFlag:
        field_list = re.findall(r'\$\{.*?\}\$', bark_robot_message_template)
        message = bark_robot_message_template
        for i in field_list:
            message = message.replace(i, str(getattr(data, i.replace('${', '').replace('}$', ''))))
        bark_message_sender(userobj.bark_url, 'LDAP请求 - Cola Dnslog', message)

def start_server():
    sk = socket.socket()
    sk.bind((LDAP_HOST, LDAP_PORT))
    sk.listen(5)

    print('[+] LDAP server listen on {}:{}'.format(LDAP_HOST, str(LDAP_PORT)))

    while True:
        conn, address = sk.accept()
        t = threading.Thread(target=link_handler, args=(conn, address))
        t.start()

if __name__ == '__main__':
    start_server()
