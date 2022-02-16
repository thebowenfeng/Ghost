import config
import random
import bitarray


port_reserve_pool = []


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def reserve_port():
    while True:
        rand_port = random.randint(config.PORT_START, config.PORT_END)
        if rand_port not in port_reserve_pool:
            port_reserve_pool.append(rand_port)
            return rand_port


def free_port(port: int):
    port_reserve_pool.remove(port)


def compare_bits(a: str, b: str):
    a_bits = bitarray.bitarray()
    b_bits = bitarray.bitarray()

    a_bits.frombytes(a.encode('utf-8'))
    b_bits.frombytes(b.encode('utf-8'))

    n_bits = 0

    for i in range(len(a_bits)):
        if i >= len(b_bits):
            break

        if a_bits[i] != b_bits[i]:
            return n_bits
        else:
            n_bits += 1

    return n_bits


def kademlia_insert(table: list, node_id: str, target_info: dict):
    similarity = compare_bits(node_id, target_info['node_id'])

    if similarity >= 254:
        table[254].append(target_info)
    else:
        table[similarity].append(target_info)


def kademlia_lookup(table: list, node_id: str, target_id: str):
    similarity = compare_bits(node_id, target_id)

    if similarity >= 254:
        return table[254]
    else:
        return table[similarity]
