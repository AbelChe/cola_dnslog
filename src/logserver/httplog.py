from http.server import BaseHTTPRequestHandler, HTTPServer

from sqlalchemy.orm import sessionmaker

from database import engine
from models import Httplog, User

import base64
from config import HTTP_HOST, HTTP_PORT

Session_class = sessionmaker(bind=engine)
Session = Session_class()

class LogHTTPHandle(BaseHTTPRequestHandler):
    def __auth(self):
        try:
            logids = next(i for i in self.path.split('/') if i)
            return logids
        except Exception as e:
            self.send_response(200)
            self.end_headers()
            return

    
    def do_HEAD(self):
        logid = self.__auth()
        try:
            self.user_selectobj = Session.query(User).filter_by(logid=logid)
            self.user_selectdata = self.user_selectobj.first()
            if not self.user_selectdata:
                self.send_response(200)
                self.end_headers()
        except Exception as e:
            self.send_response(200)
            self.end_headers()
            return
        user_agent = self.headers.get('User-Agent')
        ip_from = self.client_address[0]
        request_method = 'HEAD'
        headers = str(self.headers)
        try:
            sql_obj = Httplog(headers=headers, path=self.path, request_method=request_method, ip_from=ip_from, useragent=user_agent, owner_id=self.user_selectdata.id)
            Session.add(sql_obj)
            Session.commit()
            print('[+ SQL] path--->{} \t method--->{} \t ip--->{}'.format(self.path, request_method, ip_from))
        except Exception as e:
            Session.rollback()
            print('[SQL ERROR] ' + str(e))
            f = open('sqlerror.txt', 'a')
            f.write('path--->{} \t method--->{} \t ip--->{}'.format(self.path, request_method, ip_from))
            f.write('\n')
            f.write(str(e))
            f.write('\n----------------------------------------')
            f.close()
        finally:
            Session.close()
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        logid = self.__auth()
        try:
            self.user_selectobj = Session.query(User).filter_by(logid=logid)
            self.user_selectdata = self.user_selectobj.first()
            if not self.user_selectdata:
                self.send_response(200)
                self.end_headers()
        except Exception as e:
            self.send_response(200)
            self.end_headers()
            return
        user_agent = self.headers.get('user-agent')
        ip_from = self.client_address[0]
        request_method = 'GET'
        headers = str(self.headers)
        try:
            print(self.headers.__class__)
            sql_obj = Httplog(headers=headers, path=self.path, request_method=request_method, ip_from=ip_from, useragent=user_agent, owner_id=self.user_selectdata.id)
            Session.add(sql_obj)
            Session.commit()
            print('[+ SQL] path--->{} \t method--->{} \t ip--->{}'.format(self.path, request_method, ip_from))
        except Exception as e:
            Session.rollback()
            print('[SQL ERROR] ' + str(e))
            f = open('sqlerror.txt', 'a')
            f.write('path--->{} \t method--->{} \t ip--->{}'.format(self.path, request_method, ip_from))
            f.write('\n')
            f.write(str(e))
            f.write('\n----------------------------------------')
            f.close()
        finally:
            Session.close()
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        logid = self.__auth()
        try:
            self.user_selectobj = Session.query(User).filter_by(logid=logid)
            self.user_selectdata = self.user_selectobj.first()
            if not self.user_selectdata:
                self.send_response(200)
                self.end_headers()
        except Exception as e:
            self.send_response(200)
            self.end_headers()
            return
        user_agent = self.headers.get('User-Agent')
        ip_from = self.client_address[0]
        request_method = 'POST'
        headers = str(self.headers)
        content_length = int(self.headers.get('content-length', 0))
        ct = content_length if content_length <= 500 else 500
        body_data = base64.b64encode(self.rfile.read(ct)).decode('utf8')
        try:
            sql_obj = Httplog(headers=headers, path=self.path, content_length=content_length, body_data=body_data, request_method=request_method, ip_from=ip_from, useragent=user_agent, owner_id=self.user_selectdata.id)
            Session.add(sql_obj)
            Session.commit()
            print('[+ SQL] path--->{} \t method--->{} \t ip--->{}'.format(self.path, request_method, ip_from))
        except Exception as e:
            Session.rollback()
            print('[SQL ERROR] ' + str(e))
            f = open('sqlerror.txt', 'a')
            f.write('path--->{} \t method--->{} \t ip--->{}'.format(self.path, request_method, ip_from))
            f.write('\n')
            f.write(str(e))
            f.write('\n----------------------------------------')
            f.close()
        finally:
            Session.close()
        self.send_response(200)
        self.end_headers()


def start_server():
    http_server = HTTPServer((HTTP_HOST, HTTP_PORT), LogHTTPHandle)
    print('[+] Http server listen on {}:{}'.format(HTTP_HOST, str(HTTP_PORT)))
    http_server.serve_forever()

if __name__ == '__main__':
    start_server()
