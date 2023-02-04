#!/bin/sh

cd /coladnslog

sed -i 's!DNS_DOMAIN: .*$!DNS_DOMAIN: '${DNS_DOMAIN}'!g' config.yaml
sed -i 's!NS1_DOMAIN: .*$!NS1_DOMAIN: '${NS1_DOMAIN}'!g' config.yaml
sed -i 's!NS2_DOMAIN: .*$!NS2_DOMAIN: '${NS2_DOMAIN}'!g' config.yaml
sed -i 's!SERVER_IP: .*$!SERVER_IP: '${SERVER_IP}'!g'    config.yaml
sed -i 's!HTTP_PORT: .*$!HTTP_PORT: '${HTTP_PORT}'!g'    config.yaml
sed -i 's!HTTP_RESPONSE_SERVER_VERSION: .*$!HTTP_RESPONSE_SERVER_VERSION: '${HTTP_RESPONSE_SERVER_VERSION}'!g'    config.yaml
sed -i 's!LDAP_PORT: .*$!LDAP_PORT: '${LDAP_PORT}'!g'    config.yaml
sed -i 's!RMI_PORT: .*$!RMI_PORT: '${RMI_PORT}'!g'    config.yaml

alias python="python3.7"

nohup ./start_webserver &
nohup ./start_logserver &

tail -f /dev/null