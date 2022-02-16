import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

from Sender import Sender
from Receiver import Receiver

cred = credentials.Certificate('silence-79c33-firebase-adminsdk-dljcm-533b274b1c.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
node_list = [{}]

sender = Sender(db=db)


def reply(sender_ip, data):
    if data['type'] == 'connect':
        print(f"{sender_ip} connected")
        sender.send(sender_ip, json.dumps({"type": "get_nodes", "nodes": node_list}))
        node_list[0] = {"ip": sender_ip, "node_id": data['node_id'], "public_key": data['public_key']}
    elif data['type'] == 'get_nodes':
        sender.send(sender_ip, json.dumps({"type": "get_nodes", "nodes": node_list}))


receiver = Receiver(db=db, on_receive=reply)
receiver.listen()

while True:
    pass

