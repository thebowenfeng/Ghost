# Ghost

Ghost is a decentralized, peer to peer messaging protocol centered around privacy and anonymity. Inspired by Ethereum's Whisper protocol, Ghost provides near 100%
darkness for its users, making it extremely difficult trace individual messages and providing plausible deniability, and ensuring all messages within the network are secured with 
industry grade encryption standards.

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
