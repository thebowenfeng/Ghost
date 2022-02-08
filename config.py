import requests

HOST_IP = requests.get('https://api.ipify.org').text
OUTBOUND_PORT = 50002
INBOUND_PORT = 50001