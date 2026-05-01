#!/usr/bin/env python3

import subprocess
import random
import time
import json
from datetime import datetime

#############################################
# CONFIG
#############################################

STRESS_MODE = True

MIN_AMOUNT = 1
MAX_AMOUNT = 50

if STRESS_MODE:

    SEND_DELAY = 0.05
    MIN_CYCLE_WAIT = 5
    MAX_CYCLE_WAIT = 30

else:

    SEND_DELAY = 0.5
    MIN_CYCLE_WAIT = 10
    MAX_CYCLE_WAIT = 60


MIN_BALANCE_REQUIRED = 50
RESCUE_BALANCE = 200

TOPUP_AMOUNT = 100

LOG_FILE = "/home/ancrumar/jigocoin/tools/jgc_transfers.log"

MINER_NODES = ["node2","node7"]

MAX_REDISTRIBUTIONS = 2

#############################################
# NODOS
#############################################

NODES = {

"node1": {
    "cli": [
        "/home/ancrumar/jigocoin/build/bin/bitcoin-cli",
        "-rpcconnect=::1",
        "-rpcport=8332",
        "-datadir=/home/ancrumar/.bitcoin"
    ],
    "wallet": "miner01",
    "address": "jgc1qhunsrpechm7uudqn0c352yqaj0v78we2n7acw0"
},

"node2": {
    "cli": [
        "docker","exec",
        "jigocoin-node2",
        "/opt/jigocoin/build/bin/bitcoin-cli",
        "-datadir=/data"
    ],
    "wallet": "wallet2",
    "address": "jgc1qt68zd8pxqlyu7h9n95qm6qzgwfwf7xak49er03"
},

"node3": {
    "cli": [
        "docker","exec",
        "jigocoin-node3",
        "/opt/jigocoin/build/bin/bitcoin-cli",
        "-datadir=/data"
    ],
    "wallet": "wallet3",
    "address": "jgc1qvu6gekmsmrr8t6sea2v58q25czrthrne5mxpdk"
},

"node4": {
    "cli": [
        "ssh","hpblanco",
        "docker","exec",
        "jigocoin-node4",
        "/opt/jigocoin/build/bin/bitcoin-cli",
        "-datadir=/data"
    ],
    "wallet": "wallet4",
    "address": "jgc1qcs7jddqqu5hcgz2f4rvnm78azfdeplrmmv6mn0"
},

"node5": {
    "cli": [
        "ssh","hpblanco",
        "docker","exec",
        "jigocoin-node5",
        "/opt/jigocoin/build/bin/bitcoin-cli",
        "-datadir=/data"
    ],
    "wallet": "wallet5",
    "address": "jgc1qj55xqhh8g9ume3422lp4vhwgsh0mkxkdcgn9k9"
},

"node7": {
    "cli": [
        "ssh","hpblanco",
        "/home/ancrumar/jigocoin/bin/bitcoin-cli",
        "-datadir=/home/ancrumar/jigocoin/node7/.jigocoin"
    ],
    "wallet": "miner07",
    "address": "jgc1qfxkxlag9epatukheu90lk4ccnvpxqw84zt54fs"
}

}

#############################################

def log(msg):

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"[{ts}] {msg}"

    print(line)

    with open(LOG_FILE,"a") as f:
        f.write(line+"\n")

#############################################

def run_cli(node,args):

    cmd = NODES[node]["cli"] + args

    start = time.time()

    try:

        out = subprocess.check_output(
            cmd,
            stderr=subprocess.STDOUT,
            timeout=60
        )

        elapsed = round(time.time() - start,2)

        return out.decode().strip()

    except:

        log(f"{node}: ERROR RPC")

        return None

#############################################

def get_balance(node):

    wallet = NODES[node]["wallet"]

    out = run_cli(node,[

        f"-rpcwallet={wallet}",
        "getbalance"

    ])

    if out is None:
        return 0

    try:
        return float(out)
    except:
        return 0

#############################################

def build_balance_cache(active):

    cache = {}

    log("Cargando balance cache...")

    for node in active:

        bal = get_balance(node)

        cache[node] = bal

        log(f"{node}: {bal}")

    return cache

#############################################

def richest_node(cache):

    return max(cache,key=cache.get)

#############################################

def maintain_balances(active,cache):

    for node in active:

        if cache[node] < RESCUE_BALANCE:

            donor = richest_node(cache)

            if donor == node:
                continue

            log(f"RESCUE {donor} -> {node}")

            wallet = NODES[donor]["wallet"]

            address = NODES[node]["address"]

            run_cli(donor,[

                f"-rpcwallet={wallet}",
                "sendtoaddress",
                address,
                str(TOPUP_AMOUNT)

            ])

            cache[node] += TOPUP_AMOUNT
            cache[donor] -= TOPUP_AMOUNT

#############################################

def calculate_amount(balance):

    max_allowed = int(balance * 0.10)

    if max_allowed < MIN_AMOUNT:
        max_allowed = MIN_AMOUNT

    if max_allowed > MAX_AMOUNT:
        max_allowed = MAX_AMOUNT

    return random.randint(
        MIN_AMOUNT,
        max_allowed
    )

#############################################

def sweep_transfers(active,cache):

    total_tx = 0
    total_amount = 0

    start_sweep = time.time()

    for sender in active:

        for receiver in active:

            if sender == receiver:
                continue

            balance = cache[sender]

            amount = calculate_amount(balance)

            if balance - amount < MIN_BALANCE_REQUIRED:
                continue

            wallet = NODES[sender]["wallet"]

            address = NODES[receiver]["address"]

            log(f"{sender} -> {receiver} {amount} JGC")

            txid = run_cli(sender,[

                f"-rpcwallet={wallet}",
                "sendtoaddress",
                address,
                str(amount)

            ])

            if txid:

                log(f"TX {txid}")

                total_tx += 1
                total_amount += amount

                cache[sender] -= amount
                cache[receiver] += amount

            time.sleep(SEND_DELAY)

    total_time = round(time.time()-start_sweep,2)

    log(f"Tiempo barrido: {total_time}s")

    return total_tx,total_amount

#############################################

def main():

    log("=== ORQUESTADOR V18 INICIADO ===")

    while True:

        active = list(NODES.keys())

        cache = build_balance_cache(active)

        maintain_balances(active,cache)

        log("=== INICIO BARRIDO ===")

        tx_done,amount_done = sweep_transfers(active,cache)

        avg = 0

        if tx_done > 0:

            avg = round(amount_done / tx_done,2)

        log(

            f"=== FIN BARRIDO | "

            f"TX: {tx_done} | "

            f"Total JGC: {amount_done} | "

            f"Media: {avg}"

        )

        wait = random.randint(

            MIN_CYCLE_WAIT,
            MAX_CYCLE_WAIT

        )

        log(f"Esperando {wait}s")

        time.sleep(wait)

#############################################

if __name__ == "__main__":
    main()
