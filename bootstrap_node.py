import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from Sender import Sender
from Receiver import Receiver

cred = credentials.Certificate('silence-79c33-firebase-adminsdk-dljcm-533b274b1c.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

sender = Sender(db=db)


def reply(sender_ip, data):
    sender.send(sender_ip, "bruh")


receiver = Receiver(db=db, on_receive=reply)
receiver.listen()

