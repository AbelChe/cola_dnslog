import os
import yaml

_cola_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

configfile = open(os.path.join(_cola_dir, 'config.yaml'), 'r' ,encoding='utf-8')
CONFIG = yaml.safe_load(configfile)
configfile.close()

_db_filename = CONFIG.get('global').get('DB_FILENAME')

# Database config
DB_PATH = os.path.join(_cola_dir, _db_filename)

# DNS config
DNS_DOMAIN = CONFIG.get('logserver').get('DNS_DOMAIN')
NS1_DOMAIN = CONFIG.get('logserver').get('NS1_DOMAIN')
NS2_DOMAIN = CONFIG.get('logserver').get('NS2_DOMAIN')
SERVER_IP = CONFIG.get('logserver').get('SERVER_IP')
DNS_PORT = CONFIG.get('logserver').get('DNS_PORT')

# HTTP server config
HTTP_HOST = CONFIG.get('logserver').get('HTTP_HOST')
HTTP_PORT = CONFIG.get('logserver').get('HTTP_PORT')

# LDAP server config
LDAP_HOST = CONFIG.get('logserver').get('LDAP_HOST')
LDAP_PORT = CONFIG.get('logserver').get('LDAP_PORT')

# RMI server config
RMI_HOST = CONFIG.get('logserver').get('RMI_HOST')
RMI_PORT = CONFIG.get('logserver').get('RMI_PORT')
