import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from Sender import Sender

cred = credentials.Certificate('silence-79c33-firebase-adminsdk-dljcm-533b274b1c.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

sender = Sender(ip='testip1', message='bruh', db=db)
sender.send()