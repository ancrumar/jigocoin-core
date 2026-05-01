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

    SEND_DELAY = 0.2
    MIN_CYCLE_WAIT = 5
    MAX_CYCLE_WAIT = 30

else:

    SEND_DELAY = 0.5
    MIN_CYCLE_WAIT = 10
    MAX_CYCLE_WAIT = 60


MIN_BALANCE_REQUIRED = 50
TOPUP_AMOUNT = 100

LOG_FILE = "jgc_transfers.log"

# Nodos mineros activos
MINER_NODES = ["node2","node7"]

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
        "ssh",
        "ancrumar@192.168.68.66",
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
        "ssh",
        "ancrumar@192.168.68.66",
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

def get_mempool_size():

    out = run_cli("node1",["getmempoolinfo"])

    if out is None:
        return 0

    try:

        data = json.loads(out)

        return data["size"]

    except:

        return 0

#############################################

def wait_for_mempool(active):

    dynamic_limit = len(active) * 50

    while True:

        size = get_mempool_size()

        if size < dynamic_limit:
            return

        log(f"Mempool alto ({size}/{dynamic_limit}) esperando...")

        time.sleep(5)

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

def print_balances(active):

    log("=== BALANCES ===")

    for node in active:

        bal = get_balance(node)

        log(f"{node}: {bal} JGC")

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
# NUEVO — Redistribución desde mineros
#############################################

def redistribute_from_miners(active):

    balances = {}

    for node in active:
        balances[node] = get_balance(node)

    avg_balance = sum(balances.values()) / len(balances)

    poor_nodes = [

        n for n,b in balances.items()
        if b < avg_balance * 0.5

    ]

    rich_miners = [

        n for n,b in balances.items()
        if n in MINER_NODES and b > avg_balance * 5

    ]

    for miner in rich_miners:

        for poor in poor_nodes:

            amount = random.randint(100,300)

            log(
                f"REDISTRIBUTE {miner} -> {poor} {amount} JGC"
            )

            wallet = NODES[miner]["wallet"]

            address = NODES[poor]["address"]

            run_cli(miner,[

                f"-rpcwallet={wallet}",
                "sendtoaddress",
                address,
                str(amount)

            ])

#############################################
# NUEVO — Export CSV
#############################################

def export_csv(active,tx_done,total_amount):

    filename = "jgc_metrics.csv"

    mempool = get_mempool_size()

    balances = []

    for node in active:

        balances.append(
            str(get_balance(node))
        )

    line = ",".join([

        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        str(tx_done),
        str(total_amount),
        str(mempool),

        *balances

    ])

    try:

        with open(filename,"a") as f:

            f.write(line+"\n")

    except:

        pass

#############################################

def sweep_transfers(active):

    total_tx = 0
    total_amount = 0

    for sender in active:

        for receiver in active:

            if sender == receiver:
                continue

            wait_for_mempool(active)

            balance = get_balance(sender)

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

            time.sleep(SEND_DELAY)

    return total_tx,total_amount

#############################################

def main():

    log("=== ORQUESTADOR V16 INICIADO ===")

    while True:

        active = get_active_nodes()

        if len(active) < 2:

            log("No hay suficientes nodos activos")

            time.sleep(10)

            continue

        maintain_balances(active)

        log("=== INICIO BARRIDO ===")

        tx_done,amount_done = sweep_transfers(active)

        avg = 0

        if tx_done > 0:

            avg = round(amount_done / tx_done,2)

        log(
            f"=== FIN BARRIDO | "
            f"TX: {tx_done} | "
            f"Total JGC: {amount_done} | "
            f"Media: {avg}"
        )

        ##################################
        # NUEVAS FUNCIONES
        ##################################

        redistribute_from_miners(active)

        print_balances(active)

        export_csv(
            active,
            tx_done,
            amount_done
        )

        wait = random.randint(
            MIN_CYCLE_WAIT,
            MAX_CYCLE_WAIT
        )

        log(f"Esperando {wait}s antes del siguiente ciclo")

        time.sleep(wait)

#############################################

if __name__ == "__main__":
    main()
