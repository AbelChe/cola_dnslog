#!/bin/sh

cd /coladnslog

sed -i 's!DNS_DOMAIN: .*$!DNS_DOMAIN: '${DNS_DOMAIN}'!g' config.yaml
sed -i 's!NS1_DOMAIN: .*$!NS1_DOMAIN: '${NS1_DOMAIN}'!g' config.yaml
sed -i 's!NS2_DOMAIN: .*$!NS2_DOMAIN: '${NS2_DOMAIN}'!g' config.yaml
sed -i 's!SERVER_IP: .*$!SERVER_IP: '${SERVER_IP}'!g'    config.yaml

alias python="python3.7"

nohup ./start_webserver &
nohup ./start_logserver &

tail -f /dev/null