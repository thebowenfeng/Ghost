import config
from threading import Event
import socket

from utils import reserve_port, Colors, free_port


class Sender:
    def __init__(self, db):
        self.ip = None
        self.message = None
        self.host_ip = config.HOST_IP
        self.db = db
        self.remote_port = None
        self.answer_flag = Event()
        self.doc_ref = None
        self.outbound_port = None

    def send_offer(self):
        self.outbound_port = reserve_port()

        if not self.outbound_port:
            print(Colors.FAIL + "ERROR: No available ports at the moment" + Colors.ENDC)
            return False

        offer = {
            'sender_ip': self.host_ip,
            'receiver_ip': self.ip,
            'out_port': self.outbound_port
        }

        self.doc_ref = self.db.collection(u'offers').add({'offer': offer})
        return True

    def answer_listener(self, snapshot, changes, read_time):
        for change in changes:
            if change.type.name == "MODIFIED" and 'answer' in change.document.to_dict():
                data = change.document.to_dict()["answer"]
                self.remote_port = data['listening_port']
                self.answer_flag.set()

    def send(self, ip: str, message: str):
        self.ip = ip
        self.message = message

        if self.send_offer():
            self.db.collection(u'offers').document(self.doc_ref[1].id).on_snapshot(self.answer_listener)
            print(Colors.OKCYAN + f"LOG: Offer sent to {self.ip}" + Colors.ENDC)

            self.answer_flag.wait()
            print(Colors.OKCYAN + f"LOG: Answer received from {self.ip}. Attempting communication on remote port {self.remote_port}" + Colors.ENDC)

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('0.0.0.0', self.outbound_port))
            sock.sendto(self.message.encode(), (self.ip, self.remote_port))
            sock.shutdown(socket.SOCK_DGRAM)
            sock.close()

            print(Colors.OKCYAN + f"LOG: Sent message to {self.ip}" + Colors.ENDC)

            free_port(self.outbound_port)
