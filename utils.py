import config


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


def reserve_port(port_reserve_pool: list):
    if len(port_reserve_pool) == 0:
        port_reserve_pool.append(config.PORT_START)
        return config.PORT_START

    # Check for gaps in reserved ports
    prev = config.PORT_START
    for index in range(0, len(port_reserve_pool)):
        curr = port_reserve_pool[index]
        if curr - prev > 1:
            port_reserve_pool.insert(index, prev + 1)
            return prev + 1
        else:
            prev = curr

    # Case when all ports are consecutive, need to append
    if port_reserve_pool[-1] < config.PORT_END:
        port_reserve_pool.append(port_reserve_pool[-1] + 1)
        return port_reserve_pool[-1] + 1
    else:
        return False


def free_port(port: int, port_reserve_pool: list):
    port_reserve_pool.remove(port)
