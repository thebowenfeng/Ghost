import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
import ast
from hashlib import sha256
import time

import config
from Sender import Sender
from Receiver import Receiver
from utils import Colors, kademlia_lookup, compare_bits, kademlia_insert

cred = credentials.Certificate('silence-79c33-firebase-adminsdk-dljcm-533b274b1c.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

kademlia_table = [[] for i in range(255)]
BOOTSTRAP_NODE = "34.145.52.129"


def node_lookup(target_id: str):
    if kademlia_table == [[] for i in range(255)]:
        # Cold start scenario
        sender.send(ip=BOOTSTRAP_NODE, message=json.dumps({"type": "get_nodes"}))

    while kademlia_table == [[] for i in range(255)]:
        # Wait for nodes to be inserted
        pass
    
    lookup = kademlia_lookup(kademlia_table, node_id, target_id)
    if len(lookup) == 0:
        # Case empty row, send lookup req to nodes in closest rows
        row_num = compare_bits(node_id, target_id)
        row_dist = 1

        while row_num - row_dist >= 0 or row_num + row_dist < 255:
            if row_num - row_dist >= 0 and len(kademlia_table[row_num - row_dist]) != 0:
                for entry in kademlia_table[row_num - row_dist]:
                    sender.send(ip=entry['ip'], message=json.dumps({"type": "lookup", "target_id": target_id}))
                break
            if row_num + row_dist < 255 and len(kademlia_table[row_num + row_dist]) != 0:
                for entry in kademlia_table[row_num + row_dist]:
                    sender.send(ip=entry['ip'], message=json.dumps({"type": "lookup", "target_id": target_id}))
                break
            # If near rows are also empty, continue search
            row_dist += 1
    else:
        for entry in lookup:
            if entry['node_id'] == target_id:
                return entry
        # Can't find nodes, send lookup req to all nodes in corresponding row in kademlia table
        for entry in lookup:
            sender.send(ip=entry['ip'], message=json.dumps({"type": "lookup", "target_id": target_id}))

    return False


def on_receive(sender_ip, data):
    json_data = json.loads(data)
    if json_data["type"] == "get_nodes":
        if json_data["nodes"][0] == {}:
            pass
        else:
            for entry in json_data["nodes"]:
                kademlia_insert(kademlia_table, node_id, entry)
    elif json_data["type"] == "lookup":
        if kademlia_table == [[] for i in range(255)]:
            # Cold start scenario
            sender.send(ip=BOOTSTRAP_NODE, message=json.dumps({"type": "get_nodes"}))

        while kademlia_table == [[] for i in range(255)]:
            # Wait for nodes to be inserted
            pass

        lookup = kademlia_lookup(kademlia_table, node_id, json_data["target_id"])
        if len(lookup) == 0:
            # Similar to node lookup, if row is empty, find closest rows and send rows as lookup response
            row_num = compare_bits(node_id, json_data["target_id"])
            row_dist = 1

            while row_num - row_dist >= 0 or row_num + row_dist < 255:
                if row_num - row_dist >= 0 and len(kademlia_table[row_num - row_dist]) != 0:
                    for entry in kademlia_table[row_num - row_dist]:
                        sender.send(ip=entry['ip'], message=json.dumps(
                            {"type": "lookup_result", "nodes": kademlia_table[row_num - row_dist]}))
                    break
                if row_num + row_dist < 255 and len(kademlia_table[row_num + row_dist]) != 0:
                    for entry in kademlia_table[row_num + row_dist]:
                        sender.send(ip=entry['ip'], message=json.dumps(
                            {"type": "lookup_result", "nodes": kademlia_table[row_num + row_dist]}))
                    break
                # If near rows are also empty, continue search
                row_dist += 1
        else:
            sender.send(ip=sender_ip, message=json.dumps({"type": "lookup_result", "nodes": lookup}))
    elif json_data["type"] == "lookup_result":
        for node in json_data["nodes"]:
            kademlia_insert(kademlia_table, node_id, node)


if not os.path.isfile("private.pem") or not os.path.isfile("public.pem"):
    print(Colors.OKCYAN + "Generating keys..." + Colors.ENDC)

    private_key = RSA.generate(2048, Random.new().read)
    public_key = private_key.publickey()

    with open("private.pem", "wb") as f:
        f.write(private_key.exportKey(format='PEM'))

    with open("public.pem", "wb") as f:
        f.write(public_key.exportKey(format='PEM'))

    print(Colors.OKCYAN + "Keys generated!" + Colors.ENDC)
else:
    with open("private.pem", "rb") as f:
        private_key = RSA.importKey(f.read())

    with open("public.pem", "rb") as f:
        public_key = RSA.importKey(f.read())

node_id = sha256(public_key.exportKey(format='PEM')).hexdigest()[:20]

receiver = Receiver(db=db, on_receive=on_receive)
receiver.listen()
sender = Sender(db=db)

sender.send(BOOTSTRAP_NODE, json.dumps({"type": "connect", "node_id": node_id, "public_key": public_key.exportKey(format='PEM')}))

print(f"Node address: {node_id}")

while True:
    recv_id = input("Enter receipient ID: ")
    msg = input("Enter message: ")

    node = node_lookup(recv_id)
    start = time.time()
    while node is False:
        curr = time.time()
        if curr - start > config.LOOKUP_TIMEOUT:

            break
        node = node_lookup(recv_id)

    if node is False:
        print(Colors.FAIL + "Node lookup timed out!" + Colors.ENDC)
    else:
        print(node)
