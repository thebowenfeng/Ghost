import config
from threading import Event


class Receiver:
    def __init__(self, db, sender_init: Event, sender_finish: Event):
        self.host_ip = config.HOST_IP
        self.in_port = config.INBOUND_PORT
        self.db = db
        self.sender_init = sender_init
        self.sender_finish = sender_finish

    def offer_listener(self, snapshot, changes, read_time):
        for change in changes:
            if change.type.name == "ADDED" and 'offer' in change.document.to_dict() and 'answer' not in change.document.to_dict():
                data = change.document.to_dict()['offer']
                if data['receiver_ip'] == self.host_ip:
                    print(f"Connection received from {data['sender_ip']}. Remote outbound port: {data['out_port']}")

                print("Initiating punch...")

                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind(('0.0.0.0', config.INBOUND_PORT))
                sock.sendto(b'punch', (data['sender_ip'], data['out_port']))
                sock.close()

                print("Punching complete. Initiating listener...")
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind(('0.0.0.0', config.INBOUND_PORT))

                data = sock.recv(1024)
                print(f"Received data from {sender_ip}: {data.decode()}")

                # Forward message on (probably via Queue on main)
                    


    def listen(self):
        while True:
            self.sender_init.set()
            self.sender_finish.set()
            
            unsub = self.db.collection(u'offer').on_snapshot(self.offer_listener)
            self.sender_init.wait()
            print("Initialzed remote communication process. Temporarily stop offer listening")
            unsub.unsubscribe()
            self.sender_finish.wait()
            print("Reinstated offer listening")
