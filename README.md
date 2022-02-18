# Ghost

Ghost is a decentralized, peer to peer messaging protocol centered around privacy and anonymity. Inspired by Ethereum's Whisper protocol, Ghost provides near 100%
darkness for its users, making it extremely difficult trace individual messages and providing plausible deniability, and ensuring all messages within the network are secured with industry grade encryption standards.

### Installation and usage

Required python packages:
- pycryptodome
- firebase_admin
- bitarray

Furthermore, this protocol will not work on nodes (machines) under a network with a symmetric NAT configuration.

A firebase database credentials JSON file is required. Edit the JSON file path in line 18 of main.py

One "bootstrap" node is required. Bootstrap nodes needs to be active and accessible at all times in order for other nodes within the network to function properly. As such, 
bootstrap nodes should be ran on machines that have minimal down time, such as cloud VMs. Simply run `python bootstrap_node.py` on the machine.

Once the bootstrap node is available, replace the bootstrap node IP on line 24 in main.py, with the bootstrap machine's public IP. Then run `python main.py` on your local machine.
Machines running `main.py` are considered nodes within the network and will be able to transmit message to each other via their respective node address, which is printed on 
screen.

Within `config.py`, several settings could be manually adjusted. These include:
- `HOST_IP`. This is the public IP of your local machine. Only adjust under special circumstances.
- `PORT_START` and `PORT_END`. This is a numerical range denoting the available/free ports on your network. 
- `LOOKUP_TIMEOUT`. This represents the maximum number of seconds your node will continue to search for another node in the network until it cease the search.
- `MESSAGE_TIMEOUT`. This represents the number of seconds until messages will cease to be transmitted further within the network.

### Technical overview

Peer to peer communication is made possible using UDP hole punching. The network communication functionalities are adapted from [here](https://github.com/thebowenfeng/Python-P2P-Chat)

The core concept of Ghost is, instead of directly sending a message to the desired recipient, each node will forward the message to other nodes within the network until the message expires. To ensure plausible deniability (inability to trace the message's desired recipient), once the desired recipient receives the message, that node will continue forwarding the message to other nodes. This ensures that messages are difficult to trace, even if a third party was monitoring a node's incoming and outgoing messages.

Each message is encrypted using RSA encryption. The data is encrypted using the recipient's public key, and broadcasted into the network until it reaches the recipient, who can then decrypt the data using their private key. Nodes can check if a message is intended towards them by checking if they are able to decrypt the data using their private key.\

Each node has a unique address, which is the SHA256 hash of the first 20 characters of its public key.

Because the protcol is decentralized, public key exchange relies on node discovery algorithms, in this case a variant of the Kademlia algorithm. Each node has a table, which contains some other nodes. Each row in the table represents nodes whose address's first N bits matches the first N bits of the local node's address. As an example, if my address is `1011011....`, then node A with the address `01001011...` will be in row 0 (as A's address's bits did not align with my address's bits), and node B with the address `1010000...` will be in row 3 (as the first 3 bits of B's address matches with the first 3 bits of my address).

Upon joining the network, each node will first connect to the bootstrap node. The bootstrap node logs nodes that have previously connected to it, typically based on a certain timeframe (e.g all nodes connected in the past 24 hours), although in this case the bootstrap node only logs the last node that connects. Upon connecting, the bootstrap node will respond with all the nodes that it has logged to prevent a cold start scenario, where a new node is isolated from the rest of the nodes in the network.

To lookup a node within a table, a comparison of the bits of the local node address and the lookup node's address will yield the row in which the node should be stored, and a simple sequential search will return the node if it is stored within the table. If the node is not found, a lookup request is sent to all nodes in the same row, and they will respond with the row in which the desired node would have been stored on their respective table (by performing a lookup, described above). The process is repeatedly performed until either the search times out, or the desired node is found. If the row is empty, then the rows closeset to the initial "lookup" row is selected.

Each message is then encrypted using the public key of the recipient node, and broadcasted to every node present within the table of the sender node. The process is repeated on every node who received a message. Once a message is received by a node, it will attempt to decrypt the message using its private key. Regardless if the decryption is successful or not, the node will forward the message to all the nodes in its own table, ensuring plausible deniability. The message wlil "bounce around" within the network until it is expired. 

### Advantages

- Anonymity. Each message is completely anonymous with no way to trace its sender or desired recipient.
- Privacy. The network is completely decentralized, no 3rd party central server logs messages, making it difficult to obtain any specific message.
- Security. Each message's content is encrypted using RSA encryption and is extremely hard to be compromised.

### Disadvantage

- High computation and network cost. The broadcasting and forwarding of each message leads to unecessary computation on each node in the network.
- No guarantee a message is received. Although unlikely, it is possible for parts of the network to be isolated from each other, and thus messages unable to traverse across the network properly.
- High latency. Each message is not directly sent to the recipient, and as such the latency between sending and receiving a message is significant.

### Use cases

Ghost is designed for cases where anonymity and privacy is required, but high speed/low latency is not. Applications such as video chat or voice chat is not designed to be used with Ghost. 

