import config
import random


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
