import threading

from dnslog import start_server as dnsserver
from httplog import start_server as httpserver
from ldaplog import start_server as ldapserver
from rmilog import start_server as rmiserver

if __name__ == '__main__':
    dnslogserver = threading.Thread(name='dnslogserver',target=dnsserver)
    httplogserver = threading.Thread(name='httplogserver',target=httpserver)
    ldaplogserver = threading.Thread(name='ldaplogserver',target=ldapserver)
    rmilogserver = threading.Thread(name='rmilogserver',target=rmiserver)
    dnslogserver.start()
    httplogserver.start()
    ldaplogserver.start()
    rmilogserver.start()
    dnslogserver.join()
    httplogserver.join()
    ldaplogserver.join()
    rmilogserver.join()
