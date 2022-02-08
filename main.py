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

sender_init = Event()
sender_finish = Event()


def listen_thread():
    receiver = Receiver(db, sender_init, sender_finish)
    receiver.listen()


child_thread = threading.Thread(target=listen_thread)
child_thread.start()

sender = Sender(db=db, sender_init=sender_init, sender_finish=sender_finish)

while True:
    inp = input("Enter message: ")
    sender.send(ip="35.224.50.44", message="Bruhhhhhh")