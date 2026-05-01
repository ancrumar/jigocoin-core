#!/usr/bin/env python3

import subprocess
import time

print("\n=== CONSULTA SALDOS WALLETS JIGOCOIN ===\n")

start_total = time.time()

# --- CONFIGURACIÓN NODOS ---

nodes = {

"node1": {
"type": "local",
"wallet": "miner01"
},

"node2": {
"type": "docker_local",
"container": "jigocoin-node2",
"wallet": "wallet2"
},

"node3": {
"type": "docker_local",
"container": "jigocoin-node3",
"wallet": "wallet3"
},

"node4": {
"type": "docker_remote",
"host": "hpblanco",
"container": "jigocoin-node4",
"wallet": "wallet4"
},

"node5": {
"type": "docker_remote",
"host": "hpblanco",
"container": "jigocoin-node5",
"wallet": "wallet5"
},

"node7": {
"type": "remote_local",
"host": "hpblanco",
"wallet": "miner07",
"rpcport": "19332",
"datadir": "/home/ancrumar/jigocoin/node7/.jigocoin"
}

}

# -----------------------------------------------------

def build_command(node):

    n = nodes[node]

    if n["type"] == "local":

        return [
            "/home/ancrumar/jigocoin/build/bin/bitcoin-cli",
            "-rpcconnect=::1",
            f"-rpcwallet={n['wallet']}",
            "getbalance"
        ]

    if n["type"] == "docker_local":

        return [
            "docker","exec",
            n["container"],
            "/opt/jigocoin/build/bin/bitcoin-cli",
            "-datadir=/data",
            f"-rpcwallet={n['wallet']}",
            "getbalance"
        ]

    if n["type"] == "docker_remote":

        return [
            "ssh", n["host"],
            "docker","exec",
            n["container"],
            "/opt/jigocoin/build/bin/bitcoin-cli",
            "-datadir=/data",
            f"-rpcwallet={n['wallet']}",
            "getbalance"
        ]

    if n["type"] == "remote_local":

        return [
            "ssh", n["host"],
            "/home/ancrumar/jigocoin/bin/bitcoin-cli",
            f"-datadir={n['datadir']}",
            "-rpcconnect=127.0.0.1",
            f"-rpcport={n['rpcport']}",
            f"-rpcwallet={n['wallet']}",
            "getbalance"
        ]

# -----------------------------------------------------

def get_balance(node):

    cmd = build_command(node)

    try:

        t0 = time.time()

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        elapsed = round(time.time() - t0,2)

        if result.returncode != 0:

            return ("ERROR", elapsed)

        balance = float(result.stdout.strip())

        return (balance, elapsed)

    except Exception:

        return ("ERROR", 0)

# -----------------------------------------------------

total_balance = 0

for node in nodes:

    balance, elapsed = get_balance(node)

    if balance == "ERROR":

        print(f"{node:6} : ERROR")

    else:

        print(
            f"{node:6} : "
            f"{balance:12.2f} JGC "
            f"({elapsed}s)"
        )

        total_balance += balance

print("\n--------------------------------")

print(
    f"TOTAL RED : "
    f"{total_balance:.2f} JGC"
)

elapsed_total = round(
    time.time() - start_total,
    2
)

print(
    f"Tiempo total consulta: "
    f"{elapsed_total}s\n"
)
