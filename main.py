import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from Sender import Sender
from Receiver import Receiver

cred = credentials.Certificate('silence-79c33-firebase-adminsdk-dljcm-533b274b1c.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

receiver = Receiver(db=db, on_receive=lambda x, y: print(y))
receiver.listen()
sender = Sender(db=db)

sender.send("34.82.21.166", "Hello bootstrapnode")

while True:
    inp = input("Enter message: ")
    sender.send(ip="35.224.50.44", message=inp)
