import threading

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from Sender import Sender
from Receiver import Receiver

cred = credentials.Certificate('silence-79c33-firebase-adminsdk-dljcm-533b274b1c.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

receiver = Receiver(db=db)
receiver.listen()
sender = Sender(db=db)

while True:
    inp = input("Enter message: ")
    sender.send(ip="35.224.50.44", message=inp)
