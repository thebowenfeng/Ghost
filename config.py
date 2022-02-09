import requests

HOST_IP = requests.get('https://api.ipify.org').text
PORT_START = 55234
PORT_END = 62432
