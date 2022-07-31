import requests
import json



DINGTALK_ROBOT_API = 'https://oapi.dingtalk.com/robot/send?access_token='

def dingtalk_robot_message_sender(token, title, message):
    headers = {"Content-Type": "application/json"}
    data = {"msgtype": "markdown", "markdown": {"title": title, 'text': message}}
    requests.post('{}{}'.format(DINGTALK_ROBOT_API, token), data=json.dumps(data), headers=headers)

def bark_message_sender():
    pass