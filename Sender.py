import config
from threading import Event


class Sender:
    def __init__(self, db, sender_init: Event, sender_finish: Event):
        self.ip = None
        self.message = None
        self.host_ip = config.HOST_IP
        self.db = db
        self.remote_port = None
        self.answer_flag = Event()
        self.sender_init = sender_init
        self.sender_finish = sender_finish
        self.doc_ref = None

    def send_offer(self):
        offer = {
            'sender_ip': self.host_ip,
            'receiver_ip': self.ip,
            'out_port': config.OUTBOUND_PORT
        }

        self.doc_ref = self.db.collection(u'offers').add({'offer': offer})

    def answer_listener(self, snapshot, changes, read_time):
        for change in changes:
            if change.type.name == "MODIFIED" and 'answer' in change.document.to_dict():
                data = change.document.to_dict()["answer"]
                self.remote_port = data['listening_port']
                self.answer_flag.set()

    def send(self, ip: str, message: str):
        if self.sender_init.is_set() and self.sender_finish.is_set():
            self.ip = ip
            self.message = message
            
            self.sender_init.clear()
            self.send_offer()
            self.db.collection(u'offers').document(self.doc_ref[1].id).on_snapshot(self.answer_listener)
            print(f"Offer sent to {self.ip}")
            
            self.answer_flag.wait()
            self.answer_flag.clear()

            print(f"Answer received from {self.ip}. Attempting communication on remote port {self.remote_port}")

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('0.0.0.0', config.OUTBOUND_PORT))
            sock.sendto(msg.encode(), (self.ip, self.remote_port))

            print(f"Sent message to {self.ip}")

            self.sender_finish.clear()
        else:
            print("A separate remote communication is in progress, please wait")
