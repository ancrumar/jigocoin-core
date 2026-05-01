#!/usr/bin/env python3

import subprocess
import random
import time
import threading
import queue
from datetime import datetime
import json

LOG_FILE = "/home/ancrumar/jigocoin/tools/jgc_transfers.log"

MIN_AMOUNT = 1
MAX_AMOUNT = 50

MIN_DELAY = 0.5
MAX_DELAY = 1.5

CYCLE_MIN = 10
CYCLE_MAX = 60

MIN_BALANCE = 50
BALANCE_CACHE_TIME = 180

MAX_WORKERS = 2

REMOTE_TIMEOUT = 120

# --- FEES ADAPTATIVAS ---

BASE_FEE_MIN = 0.00000800
BASE_FEE_MAX = 0.00001800

balance_cache = {}
balance_cache_time = {}

remote_lock = threading.Lock()

# Histórico mempool
mempool_history = []

# --- CONFIGURACIÓN NODOS ---

nodes = {

"node1": {
"type": "local",
"wallet": "miner01",
"address": "jgc1qhunsrpechm7uudqn0c352yqaj0v78we2n7acw0"
},

"node2": {
"type": "docker_local",
"container": "jigocoin-node2",
"wallet": "wallet2",
"address": "jgc1qt68zd8pxqlyu7h9n95qm6qzgwfwf7xak49er03"
},

"node3": {
"type": "docker_local",
"container": "jigocoin-node3",
"wallet": "wallet3",
"address": "jgc1qvu6gekmsmrr8t6sea2v58q25czrthrne5mxpdk"
},

"node4": {
"type": "docker_remote",
"host": "hpblanco",
"container": "jigocoin-node4",
"wallet": "wallet4",
"address": "jgc1qcs7jddqqu5hcgz2f4rvnm78azfdeplrmmv6mn0"
},

"node5": {
"type": "docker_remote",
"host": "hpblanco",
"container": "jigocoin-node5",
"wallet": "wallet5",
"address": "jgc1qj55xqhh8g9ume3422lp4vhwgsh0mkxkdcgn9k9"
},

"node7": {
"type": "remote_local",
"host": "hpblanco",
"wallet": "miner07",
"address": "jgc1qfxkxlag9epatukheu90lk4ccnvpxqw84zt54fs",
"rpcport": "19332",
"datadir": "/home/ancrumar/jigocoin/node7/.jigocoin"
}

}

# -----------------------------------------------------

def log(msg):

    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"

    print(line)

    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# -----------------------------------------------------

def build_command(node, rpc):

    n = nodes[node]

    if n["type"] == "local":

        return [
            "/home/ancrumar/jigocoin/build/bin/bitcoin-cli",
            "-rpcconnect=::1",
            f"-rpcwallet={n['wallet']}"
        ] + rpc

    if n["type"] == "docker_local":

        return [
            "docker","exec",
            n["container"],
            "/opt/jigocoin/build/bin/bitcoin-cli",
            "-datadir=/data",
            f"-rpcwallet={n['wallet']}"
        ] + rpc

    if n["type"] == "docker_remote":

        return [
            "ssh", n["host"],
            "docker","exec",
            n["container"],
            "/opt/jigocoin/build/bin/bitcoin-cli",
            "-datadir=/data",
            f"-rpcwallet={n['wallet']}"
        ] + rpc

    if n["type"] == "remote_local":

        return [
            "ssh", n["host"],
            "/home/ancrumar/jigocoin/bin/bitcoin-cli",
            f"-datadir={n['datadir']}",
            "-rpcconnect=127.0.0.1",
            f"-rpcport={n['rpcport']}",
            f"-rpcwallet={n['wallet']}"
        ] + rpc

# -----------------------------------------------------

def run_rpc(node, rpc):

    cmd = build_command(node, rpc)

    try:

        if nodes[node]["type"] in ["docker_remote","remote_local"]:

            with remote_lock:

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=REMOTE_TIMEOUT
                )

        else:

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

        if result.returncode != 0:

            log(f"{node}: ERROR {result.stderr.strip()}")
            return None

        return result.stdout.strip()

    except Exception as e:

        log(f"{node}: EXCEPTION {str(e)}")
        return None

# -----------------------------------------------------

def get_balance(node):

    now = time.time()

    if node in balance_cache:

        if now - balance_cache_time[node] < BALANCE_CACHE_TIME:

            return balance_cache[node]

    r = run_rpc(node, ["getbalance"])

    if r is None:
        return 0

    bal = float(r)

    balance_cache[node] = bal
    balance_cache_time[node] = now

    return bal

# -----------------------------------------------------

def get_mempool_size():

    r = run_rpc("node1", ["getmempoolinfo"])

    if not r:
        return 0

    try:

        data = json.loads(r)

        size = data["size"]

        mempool_history.append(size)

        if len(mempool_history) > 50:
            mempool_history.pop(0)

        return size

    except:

        return 0

# -----------------------------------------------------

def adaptive_delay():

    size = get_mempool_size()

    if size > 600:
        return random.uniform(2.0,3.0)

    elif size > 300:
        return random.uniform(1.5,2.5)

    elif size > 150:
        return random.uniform(1.0,2.0)

    else:
        return random.uniform(
            MIN_DELAY,
            MAX_DELAY
        )

# -----------------------------------------------------

def calculate_fee():

    if not mempool_history:
        fee = random.uniform(BASE_FEE_MIN, BASE_FEE_MAX)

    else:

        size = mempool_history[-1]

        if size < 100:

            fee_min = BASE_FEE_MIN
            fee_max = BASE_FEE_MAX * 0.8

        elif size < 250:

            fee_min = BASE_FEE_MIN * 1.2
            fee_max = BASE_FEE_MAX

        elif size < 500:

            fee_min = BASE_FEE_MIN * 1.5
            fee_max = BASE_FEE_MAX * 1.5

        else:

            fee_min = BASE_FEE_MIN * 2
            fee_max = BASE_FEE_MAX * 2

        fee = random.uniform(fee_min, fee_max)

    return round(fee, 8)

# -----------------------------------------------------

def log_mempool():

    if not mempool_history:
        return

    size = mempool_history[-1]

    avg = round(
        sum(mempool_history) /
        len(mempool_history),
        1
    )

    max_seen = max(mempool_history)

    log(
        f"Mempool size: {size} "
        f"(avg: {avg} | max: {max_seen})"
    )

# -----------------------------------------------------

def log_difficulty():

    r = run_rpc("node1", ["getblockchaininfo"])

    if not r:
        return

    try:

        data = json.loads(r)

        diff = data["difficulty"]

        log(f"Difficulty: {diff}")

    except:

        log("Difficulty read error")

# -----------------------------------------------------

def log_balances():

    log("=== BALANCES ===")

    for node in nodes:

        bal = get_balance(node)

        log(f"{node}: {round(bal,8)} JGC")

# -----------------------------------------------------

def send_tx(src, dst):

    addr = nodes[dst]["address"]

    amount = random.randint(
        MIN_AMOUNT,
        MAX_AMOUNT
    )

    bal = get_balance(src)

    if bal < amount + MIN_BALANCE:

        log(f"{src}: saldo bajo ({bal})")
        return

    fee = calculate_fee()

    fee_str = f"{fee:.8f}"

    log(
        f"{src} -> {dst} {amount} JGC "
        f"| fee={fee_str}"
    )

    r = run_rpc(
        src,
        [
            "sendtoaddress",
            addr,
            str(amount),
            "",
            "",
            "false",
            fee_str
        ]
    )

    if r:

        log(f"TX {r}")

# -----------------------------------------------------

def worker(q):

    while True:

        src, dst = q.get()

        try:

            send_tx(src, dst)

            time.sleep(
                adaptive_delay()
            )

        finally:

            q.task_done()

# -----------------------------------------------------

def main():

    log("=== ORQUESTADOR V22.1 INICIADO ===")

    q = queue.Queue()

    for _ in range(MAX_WORKERS):

        t = threading.Thread(
            target=worker,
            args=(q,),
            daemon=True
        )

        t.start()

    while True:

        start = time.time()

        log("=== INICIO BARRIDO ===")

        node_list = list(nodes.keys())

        for src in node_list:

            for dst in node_list:

                if src != dst:

                    q.put((src, dst))

        q.join()

        elapsed = round(
            time.time() - start,
            2
        )

        log(f"Tiempo barrido: {elapsed}s")

        get_mempool_size()

        log_mempool()

        log_difficulty()

        log_balances()

        delay = random.randint(
            CYCLE_MIN,
            CYCLE_MAX
        )

        log(f"Esperando {delay}s")

        time.sleep(delay)

# -----------------------------------------------------

if __name__ == "__main__":

    main()
