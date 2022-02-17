import config
import socket
import time
from threading import Thread

from utils import reserve_port, Colors, free_port


class Receiver:
    def __init__(self, db, on_receive: callable):
        self.host_ip = config.HOST_IP
        self.inbound_port = None
        self.db = db
        self.receive_callback = on_receive

    def offer_listener(self, snapshot, changes, read_time):
        for change in changes:
            if change.type.name == "ADDED" and 'offer' in change.document.to_dict() and 'answer' not in change.document.to_dict():
                data = change.document.to_dict()['offer']
                if data['receiver_ip'] == self.host_ip:
                    #print(Colors.OKCYAN + f"Connection received from {data['sender_ip']}. Remote outbound port: {data['out_port']}" + Colors.ENDC)

                    sender_ip = data['sender_ip']
                    self.inbound_port = reserve_port()

                    if not self.inbound_port:
                        print(Colors.FAIL + "ERROR: No port available at the moment" + Colors.ENDC)
                    else:
                        #print(Colors.OKCYAN + "LOG: Initiating punch..." + Colors.ENDC)

                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.bind(('0.0.0.0', self.inbound_port))
                        sock.sendto(b'punch', (data['sender_ip'], data['out_port']))
                        sock.close()

                        #print(Colors.OKCYAN + "LOG: Punching complete" + Colors.ENDC)

                        time.sleep(0.5)

                        #print(Colors.OKCYAN + "LOG: Sending answer..." + Colors.ENDC)
                        answer = {
                            'listening_port': self.inbound_port
                        }
                        self.db.collection(u'offers').document(change.document.id).update({"answer": answer})
                        #print(Colors.OKCYAN + f"LOG: Answer sent, listening on {self.inbound_port}" + Colors.ENDC)

                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.bind(('0.0.0.0', self.inbound_port))

                        data = sock.recv(1024)
                        #print(Colors.OKCYAN + f"LOG: Received data from {sender_ip}" + Colors.ENDC)
                        sock.close()

                        free_port(self.inbound_port)

                        callback_thread = Thread(target=self.receive_callback, args=(sender_ip, data))
                        callback_thread.start()

    def listen(self):
        unsub = self.db.collection(u'offers').on_snapshot(self.offer_listener)
