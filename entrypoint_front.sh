#!/bin/sh

env | grep API_BASE_URL
cd /var/www/html/static/js/
sed -i 's!baseURL:\".*\",timeout!baseURL:\"'${API_BASE_URL}'\",timeout!g' app.????????.js

nginx -c /etc/nginx/nginx.conf
nginx -s reload

tail -f /dev/null