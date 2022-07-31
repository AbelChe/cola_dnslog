import os
import yaml

_cola_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

configfile = open(os.path.join(_cola_dir, 'config.yaml'), 'r' ,encoding='utf-8')
CONFIG = yaml.safe_load(configfile)
configfile.close()

_db_filename = CONFIG.get('global').get('DB_FILENAME')

# Database config
DB_PATH = os.path.join(_cola_dir, _db_filename)

# password md5 salt
PASSWORD_SALT = CONFIG.get('webserver').get('PASSWORD_SALT')

# Fastapi server
HOST = CONFIG.get('webserver').get('HOST')
PORT = CONFIG.get('webserver').get('PORT')

# Server info
DNS_DOMAIN = CONFIG.get('logserver').get('DNS_DOMAIN')
SERVER_IP = CONFIG.get('logserver').get('SERVER_IP')
HTTP_PORT = CONFIG.get('logserver').get('HTTP_PORT')
LDAP_PORT = CONFIG.get('logserver').get('LDAP_PORT')
RMI_PORT = CONFIG.get('logserver').get('RMI_PORT')