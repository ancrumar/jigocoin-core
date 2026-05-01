#!/usr/bin/env python3

import subprocess
import time
import random
import threading
from queue import Queue
from datetime import datetime

# ===============================
# CONFIG
# ===============================

LOG_FILE = "/home/ancrumar/jigocoin/tools/jgc_transfers.log"

MIN_BALANCE = 50
RESCUE_AMOUNT = 100

MIN_DELAY_CYCLE = 10
MAX_DELAY_CYCLE = 60

MIN_SEND = 1
MAX_SEND = 50

# ===============================
# CLI COMMANDS
# ===============================

LOCAL_CLI = [
    "/home/ancrumar/jigocoin/build/bin/bitcoin-cli",
    "-rpcconnect=::1"
]

REMOTE_NODE4 = [
    "ssh","hpblanco",
    "docker","exec","jigocoin-node4",
    "/opt/jigocoin/build/bin/bitcoin-cli",
    "-datadir=/data",
    "-rpcwallet=wallet4"
]

REMOTE_NODE5 = [
    "ssh","hpblanco",
    "docker","exec","jigocoin-node5",
    "/opt/jigocoin/build/bin/bitcoin-cli",
    "-datadir=/data",
    "-rpcwallet=wallet5"
]

REMOTE_NODE7 = [
    "ssh","hpblanco",
    "/home/ancrumar/jigocoin/bin/bitcoin-cli",
    "-datadir=/home/ancrumar/jigocoin/node7/.jigocoin"
]

# ===============================
# NODES
# ===============================

NODES = {

"node1": {
    "wallet":"wallet1",
    "address":"jgc1qhunsrpechm7uudqn0c352yqaj0v78we2n7acw0",
    "cmd":LOCAL_CLI
},

"node2": {
    "wallet":"wallet2",
    "address":"jgc1qt68zd8pxqlyu7h9n95qm6qzgwfwf7xak49er03",
    "cmd":LOCAL_CLI
},

"node3": {
    "wallet":"wallet3",
    "address":"jgc1qvu6gekmsmrr8t6sea2v58q25czrthrne5mxpdk",
    "cmd":LOCAL_CLI
},

"node4": {
    "wallet":"wallet4",
    "address":"jgc1qhunsrpechm7uudqn0c352yqaj0v78we2n7acw0",
    "cmd":REMOTE_NODE4
},

"node5": {
    "wallet":"wallet5",
    "address":"jgc1qt68zd8pxqlyu7h9n95qm6qzgwfwf7xak49er03",
    "cmd":REMOTE_NODE5
},

"node7": {
    "wallet":"miner07",
    "address":"jgc1qvu6gekmsmrr8t6sea2v58q25czrthrne5mxpdk",
    "cmd":REMOTE_NODE7
}

}

MINER_NODES = ["node2","node7"]

# ===============================
# LOGGING
# ===============================

def log(msg):

    ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    line = f"{ts} {msg}"

    print(line)

    with open(LOG_FILE,"a") as f:
        f.write(line+"\n")

# ===============================
# RPC
# ===============================

def rpc(node,args):

    base = NODES[node]["cmd"]

    wallet = NODES[node]["wallet"]

    cmd = base + ["-rpcwallet="+wallet] + args

    try:

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:

            log(f"{node}: ERROR {result.stderr}")

            return None

        return result.stdout.strip()

    except subprocess.TimeoutExpired:

        log(f"{node}: TIMEOUT")

        return None

# ===============================
# MEMPOOL
# ===============================

def get_mempool():

    cmd = LOCAL_CLI + ["getmempoolinfo"]

    try:

        r = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        txt = r.stdout

        size = int(txt.split('"size":')[1].split(",")[0])

        return size

    except:

        return 0

# ===============================
# WORKERS
# ===============================

def determine_workers():

    mem = get_mempool()

    if mem > 250:
        return 1

    if mem > 150:
        return 2

    return 3

# ===============================
# BALANCES
# ===============================

def load_balance_cache():

    cache = {}

    log("Cargando balance cache...")

    for n in NODES:

        bal = rpc(n,["getbalance"])

        if bal is None:
            cache[n]=0
        else:
            cache[n]=float(bal)

        log(f"{n}: {cache[n]}")

    return cache

# ===============================
# RESCUE
# ===============================

def rescue_nodes(cache):

    richest = max(cache,key=cache.get)

    for n in cache:

        if cache[n] < MIN_BALANCE:

            if richest == n:
                continue

            log(f"RESCUE {richest} -> {n}")

            addr = NODES[n]["address"]

            rpc(
                richest,
                ["sendtoaddress",addr,str(RESCUE_AMOUNT)]
            )

# ===============================
# WORKER
# ===============================

def worker(queue,cache):

    while True:

        sender,receiver = queue.get()

        try:

            bal = cache.get(sender,0)

            amount = random.randint(
                MIN_SEND,
                MAX_SEND
            )

            if sender not in MINER_NODES:

                if bal < MIN_BALANCE + amount:
                    continue

            addr = NODES[receiver]["address"]

            log(f"{sender} -> {receiver} {amount} JGC")

            tx = rpc(
                sender,
                ["sendtoaddress",
                 addr,
                 str(amount)]
            )

            if tx:
                log(f"TX {tx}")

        except Exception as e:

            log(f"{sender}: ERROR worker {e}")

        finally:

            queue.task_done()

# ===============================
# SWEEP
# ===============================

def sweep_parallel(cache):

    start = time.time()

    queue = Queue()

    for s in NODES:

        for r in NODES:

            if s != r:

                queue.put((s,r))

    workers = determine_workers()

    log(f"Workers activos: {workers}")

    for i in range(workers):

        t = threading.Thread(
            target=worker,
            args=(queue,cache),
            daemon=True
        )

        t.start()

    queue.join()

    elapsed = round(
        time.time()-start,
        2
    )

    log(f"Tiempo barrido: {elapsed}s")

# ===============================
# MAIN LOOP
# ===============================

def main():

    log("=== ORQUESTADOR V19.4 INICIADO ===")

    while True:

        cache = load_balance_cache()

        rescue_nodes(cache)

        log("=== INICIO BARRIDO ===")

        sweep_parallel(cache)

        delay = random.randint(
            MIN_DELAY_CYCLE,
            MAX_DELAY_CYCLE
        )

        log(f"Esperando {delay}s")

        time.sleep(delay)

# ===============================

if __name__ == "__main__":

    main()
