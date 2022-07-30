import datetime
import socket
import threading

from sqlalchemy.orm import sessionmaker

from config import RMI_HOST, RMI_PORT
from database import engine
from models import Rmilog, User

RMI_FINGERPRINT = b'\x4a\x52\x4d\x49\x00\x02\x4b'
RMI_RETURN_1 = b'\x4e\x00\x0e\x31\x34\x2e\x31\x34\x39\x2e\x31\x35\x33\x2e\x32\x31\x32\x00\x00\x2f\xc9'
RMI_RETUEN_2 = b''

Session_class = sessionmaker(bind=engine)
Session = Session_class()

def link_handler(link, client):
    print("[R] Receive from {}:{}".format(client[0], client[1]))
    while True:
        client_data1 = link.recv(1024)
        if client_data1 == RMI_FINGERPRINT:
            # print(' [+] Received ldap package 1')
            link.send(RMI_RETURN_1)
            client_data2 = link.recv(1024)
            # check the second package
            rmi_ip_range = client_data2[1]
            rmi_ip = client_data2[2:2+rmi_ip_range].decode('utf8')
            print(' [+] Get RMI client ip: ' + rmi_ip)
            if len(client_data2) == 17:
                link.send(RMI_RETUEN_2)
                client_data3 = link.recv(1024)
            else:
                client_data3 = client_data2[17::]
            java_seaialize = client_data3[1::]
            java_seaialize_contents_TC_BLOCKDATA_length = java_seaialize[5]
            java_serialize_contents_TC_STRING = java_seaialize[6+java_seaialize_contents_TC_BLOCKDATA_length::]
            java_serialize_contents_TC_STRING_length = java_serialize_contents_TC_STRING[2]
            if len(java_serialize_contents_TC_STRING) != java_serialize_contents_TC_STRING_length+3:
                break
            path = java_serialize_contents_TC_STRING[-1*java_serialize_contents_TC_STRING_length::].decode()
            print(' [{}] Path: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), path))
            logid = path[-3::]
            try:
                if len(logid) != 3:
                    break
                user_selectobj = Session.query(User).filter_by(logid=logid)
                user_selectdata = user_selectobj.first()
                if user_selectdata:
                    sql_obj = Rmilog(objectname=path, rmi_client_ip=rmi_ip, ip_from=client[0], owner_id=user_selectdata.id)
                    Session.add(sql_obj)
                    Session.commit()
                    print('[+ SQL] objectname--->{} \t type--->{} \t rmi_clientip--->{} \t ip--->{}'.format(path, 'RMI', rmi_ip, client[0]))
            except Exception as e:
                Session.rollback()
                print('[SQL ERROR] ' + path + ' ' + str(e))
                f = open('sqlerror.txt', 'a')
                f.write('[+ SQL] objectname--->{} \t type--->{} \t ip--->{}'.format(path, 'RMI', client[0]))
                f.write('\n')
                f.write(str(e))
                f.write('\n----------------------------------------')
                f.close()
            finally:
                Session.close()
            break
        break
    link.close()


def start_server():
    sk = socket.socket()
    sk.bind((RMI_HOST, RMI_PORT))
    sk.listen(5)

    print('[+] RMI server listen on {}:{}'.format(RMI_HOST, str(RMI_PORT)))

    while True:
        conn, address = sk.accept()
        t = threading.Thread(target=link_handler, args=(conn, address))
        t.start()

if __name__ == '__main__':
    start_server()
