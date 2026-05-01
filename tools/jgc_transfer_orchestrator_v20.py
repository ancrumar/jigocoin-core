#!/usr/bin/env python3

import subprocess
import random
import time
import threading
import queue
import json
from datetime import datetime

# =========================
# CONFIGURACIÓN GLOBAL
# =========================

LOG_FILE = "/home/ancrumar/jigocoin/tools/jgc_transfers.log"

MIN_AMOUNT = 1
MAX_AMOUNT = 50

MIN_DELAY = 0.5
MAX_DELAY = 1.5

CYCLE_MIN = 10
CYCLE_MAX = 60

MIN_BALANCE = 50
RESCUE_AMOUNT = 100

MEMPOOL_LIMIT = 300

MAX_WORKERS = 4

# =========================
# NODOS REALES
# =========================

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
        "rpcport": "19332"
    }

}

# =========================
# LOG
# =========================

def log(msg):

    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"

    print(line)

    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# =========================
# COMANDO RPC
# =========================

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
            "docker", "exec",
            n["container"],
            "/opt/jigocoin/build/bin/bitcoin-cli",
            "-datadir=/data",
            f"-rpcwallet={n['wallet']}"
        ] + rpc

    if n["type"] == "docker_remote":

        return [
            "ssh", n["host"],
            "docker", "exec",
            n["container"],
            "/opt/jigocoin/build/bin/bitcoin-cli",
            "-datadir=/data",
            f"-rpcwallet={n['wallet']}"
        ] + rpc

    if n["type"] == "remote_local":

        return [
            "ssh", n["host"],
            "/home/ancrumar/jigocoin/bin/bitcoin-cli",
            "-rpcconnect=127.0.0.1",
            f"-rpcport={n['rpcport']}",
            f"-rpcwallet={n['wallet']}"
        ] + rpc

# =========================
# RPC EXEC
# =========================

def run_rpc(node, rpc):

    cmd = build_command(node, rpc)

    try:

        start = time.time()

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        elapsed = round(time.time() - start, 2)

        if result.returncode != 0:

            log(f"{node}: ERROR {result.stderr.strip()}")
            return None

        return result.stdout.strip()

    except Exception as e:

        log(f"{node}: EXCEPTION {str(e)}")
        return None

# =========================
# BALANCE
# =========================

def get_balance(node):

    r = run_rpc(node, ["getbalance"])

    if r is None:
        return 0

    return float(r)

# =========================
# MEMPOOL
# =========================

def mempool_size():

    r = run_rpc("node1", ["getmempoolinfo"])

    if r is None:
        return 0

    j = json.loads(r)

    return j["size"]

# =========================
# RESCUE
# =========================

def rescue(target):

    balances = {}

    for n in nodes:

        balances[n] = get_balance(n)

    richest = max(balances, key=balances.get)

    if richest == target:
        return

    log(f"RESCUE {richest} -> {target}")

    addr = nodes[target]["address"]

    run_rpc(
        richest,
        ["sendtoaddress", addr, str(RESCUE_AMOUNT)]
    )

# =========================
# SEND TX
# =========================

def send_tx(src, dst):

    addr = nodes[dst]["address"]

    amount = random.randint(
        MIN_AMOUNT,
        MAX_AMOUNT
    )

    bal = get_balance(src)

    if bal < amount + MIN_BALANCE:

        log(f"{src}: saldo bajo ({bal})")

        rescue(src)
        return

    log(f"{src} -> {dst} {amount} JGC")

    r = run_rpc(
        src,
        ["sendtoaddress", addr, str(amount)]
    )

    if r:

        log(f"TX {r}")

# =========================
# WORKER
# =========================

def worker(q):

    while True:

        src, dst = q.get()

        try:

            if mempool_size() > MEMPOOL_LIMIT:

                log("Mempool alta, pausa")

                time.sleep(5)

            send_tx(src, dst)

            time.sleep(
                random.uniform(
                    MIN_DELAY,
                    MAX_DELAY
                )
            )

        finally:

            q.task_done()

# =========================
# MAIN
# =========================

def main():

    log("=== ORQUESTADOR V20 INICIADO ===")

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

        delay = random.randint(
            CYCLE_MIN,
            CYCLE_MAX
        )

        log(f"Esperando {delay}s")

        time.sleep(delay)

if __name__ == "__main__":

    main()
