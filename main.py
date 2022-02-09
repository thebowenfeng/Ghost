import threading

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from threading import Event

from Sender import Sender
from Receiver import Receiver

cred = credentials.Certificate('silence-79c33-firebase-adminsdk-dljcm-533b274b1c.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
port_reserve_pool = []


def listen_thread():
    receiver = Receiver(db)
    receiver.listen()


child_thread = threading.Thread(target=listen_thread)
child_thread.start()

sender = Sender(db=db)

while True:
    inp = input("Enter message: ")
    sender.send(ip="35.224.50.44", message=inp)
