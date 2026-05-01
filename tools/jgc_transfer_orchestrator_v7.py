#!/usr/bin/env python3

import subprocess
import random
import time
from datetime import datetime

#############################################
# CONFIG GLOBAL
#############################################

MIN_AMOUNT = 1
MAX_AMOUNT = 20

MIN_WAIT_MIN = 1
MAX_WAIT_MIN = 15

MIN_BALANCE_REQUIRED = 50
TOPUP_AMOUNT = 100

LOG_FILE = "jgc_transfers.log"

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
        "ssh",
        "ancrumar@192.168.68.66",
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

    try:

        out = subprocess.check_output(
            cmd,
            stderr=subprocess.STDOUT
        )

        return out.decode().strip()

    except:

        return None

#############################################

def node_alive(node):

    r = run_cli(node,["getblockcount"])

    return r is not None

#############################################

def get_active_nodes():

    active = []

    for node in NODES:

        if node_alive(node):

            active.append(node)

        else:

            log(f"{node}: OFFLINE")

    return active

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

def richest_node(active):

    balances = {}

    for node in active:

        balances[node] = get_balance(node)

    return max(
        balances,
        key=balances.get
    )

#############################################

def maintain_balances(active):

    for node in active:

        balance = get_balance(node)

        if balance < MIN_BALANCE_REQUIRED:

            donor = richest_node(active)

            if donor == node:
                continue

            log(f"TOP-UP {donor} -> {node}")

            wallet = NODES[donor]["wallet"]

            address = NODES[node]["address"]

            run_cli(donor,[
                f"-rpcwallet={wallet}",
                "sendtoaddress",
                address,
                str(TOPUP_AMOUNT)
            ])

#############################################

def random_transfer(active):

    if len(active) < 2:
        return

    sender = random.choice(active)

    receiver = sender

    while receiver == sender:

        receiver = random.choice(active)

    amount = random.randint(
        MIN_AMOUNT,
        MAX_AMOUNT
    )

    balance = get_balance(sender)

    if balance < amount:
        return

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

#############################################

def main():

    log("=== ORQUESTADOR V7 INICIADO ===")

    while True:

        active = get_active_nodes()

        if not active:

            log("No hay nodos activos")

            time.sleep(30)

            continue

        maintain_balances(active)

        random_transfer(active)

        wait = random.randint(
            MIN_WAIT_MIN,
            MAX_WAIT_MIN
        )

        log(f"Esperando {wait} min")

        time.sleep(wait*60)

#############################################

if __name__ == "__main__":
    main()
