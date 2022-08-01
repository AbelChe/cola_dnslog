import json
from urllib.parse import quote, urljoin

import requests

DINGTALK_ROBOT_API = 'https://oapi.dingtalk.com/robot/send?access_token='

def dingtalk_robot_message_sender(token, title, message):
    headers = {"Content-Type": "application/json"}
    data = {"msgtype": "markdown", "markdown": {"title": title, 'text': message}}
    requests.post('{}{}'.format(DINGTALK_ROBOT_API, token), data=json.dumps(data), headers=headers)

def bark_message_sender(server_url, title, message):
    title = quote(title, safe='')
    message = quote(message, safe='')
    url1 = urljoin(server_url + '/', title)
    url2 = urljoin(url1 + '/', message)
    requests.get(url2)
