import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

from Sender import Sender
from Receiver import Receiver

cred = credentials.Certificate('silence-79c33-firebase-adminsdk-dljcm-533b274b1c.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def on_receive(sender_ip, data):
    json_data = json.loads(data)
    if json_data["type"] == "get_nodes":
        print(json_data["nodes"])


receiver = Receiver(db=db, on_receive=on_receive)
receiver.listen()
sender = Sender(db=db)

sender.send("34.82.21.166", "Hello bootstrapnode")

while True:
    inp = input("Enter message: ")
    sender.send(ip="35.224.50.44", message=inp)
