#!/usr/bin/env python3

import subprocess
import csv
from collections import defaultdict

CSV_FILE = "/home/ancrumar/jigocoin_blocks.csv"

print("\n=== BUSQUEDA REAL DE DIRECCIONES ===\n")

# ---------------------------------------
# LEER CSV
# ---------------------------------------

address_totals = defaultdict(float)

with open(CSV_FILE) as f:

    reader = csv.DictReader(f, delimiter=';')

    for row in reader:

        addr = row["miner_address"]
        reward = float(row["reward"])

        address_totals[addr] += reward

print(f"Direcciones detectadas: {len(address_totals)}\n")

# ---------------------------------------
# FUNCION PARA PROBAR ADDRESS
# ---------------------------------------

def check_address(cmd_base, addr):

    try:

        cmd = f"{cmd_base} getaddressinfo {addr}"

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        if '"ismine": true' in result.stdout:

            return True

    except:
        pass

    return False

# ---------------------------------------
# NODOS
# ---------------------------------------

nodes = [

    {
        "name": "node1",
        "cmd": "~/jigocoin/build/bin/bitcoin-cli -rpcwallet=miner01"
    },

    {
        "name": "node2",
        "cmd": "docker exec jigocoin-node2 /opt/jigocoin/build/bin/bitcoin-cli -datadir=/data -rpcwallet=wallet2"
    },

    {
        "name": "node3",
        "cmd": "docker exec jigocoin-node3 /opt/jigocoin/build/bin/bitcoin-cli -datadir=/data -rpcwallet=wallet3"
    },

    {
        "name": "node4",
        "cmd": "~/jigocoin/build/bin/bitcoin-cli -rpcwallet=wallet4"
    },

    {
        "name": "node5",
        "cmd": "~/jigocoin/build/bin/bitcoin-cli -rpcwallet=wallet5"
    },

    {
        "name": "node7",
        "cmd": "/home/ancrumar/jigocoin/bin/bitcoin-cli -datadir=/home/ancrumar/jigocoin/node7/.jigocoin -rpcwallet=miner07"
    }

]

print("\n=== BUSCANDO DIRECCIONES ===\n")

found_total = 0

for addr, amount in sorted(
        address_totals.items(),
        key=lambda x: x[1],
        reverse=True):

    found = None

    for node in nodes:

        if check_address(node["cmd"], addr):

            found = node["name"]
            break

    if found:

        found_total += amount

        print(
            f"{addr}  "
            f"{amount:12.2f} JGC  "
            f"→ {found}"
        )

    else:

        print(
            f"{addr}  "
            f"{amount:12.2f} JGC  "
            f"⚠️ NO ENCONTRADA"
        )

print("\n--------------------------------")

print(f"TOTAL LOCALIZADO : {found_total:.2f} JGC")

print("\n=== FIN ===\n")
