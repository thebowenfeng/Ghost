import requests

HOST_IP = requests.get('https://api.ipify.org').text
PORT_START = 50000
PORT_END = 60000

LOOKUP_TIMEOUT = 10
MESSAGE_TIMEOUT = 10
