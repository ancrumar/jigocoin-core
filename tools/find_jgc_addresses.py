#!/usr/bin/env python3

import subprocess
import csv
from collections import defaultdict

CSV_FILE = "/home/ancrumar/jigocoin_blocks.csv"

print("\n=== ANALISIS DIRECCIONES JIGOCOIN ===\n")

# ---------------------------------------
# LEER CSV (con separador ;)
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
# NODOS A CONSULTAR
# ---------------------------------------

nodes = [

    {
        "name": "node1",
        "cmd": "~/jigocoin/build/bin/bitcoin-cli -rpcwallet=miner01 listreceivedbyaddress 0 true"
    },

    {
        "name": "node2",
        "cmd": "docker exec jigocoin-node2 /opt/jigocoin/build/bin/bitcoin-cli -datadir=/data -rpcwallet=wallet2 listreceivedbyaddress 0 true"
    },

    {
        "name": "node3",
        "cmd": "docker exec jigocoin-node3 /opt/jigocoin/build/bin/bitcoin-cli -datadir=/data -rpcwallet=wallet3 listreceivedbyaddress 0 true"
    },

    {
        "name": "node4",
        "cmd": "~/jigocoin/build/bin/bitcoin-cli -rpcwallet=wallet4 listreceivedbyaddress 0 true"
    },

    {
        "name": "node5",
        "cmd": "~/jigocoin/build/bin/bitcoin-cli -rpcwallet=wallet5 listreceivedbyaddress 0 true"
    },

    {
        "name": "node7",
        "cmd": "/home/ancrumar/jigocoin/bin/bitcoin-cli -datadir=/home/ancrumar/jigocoin/node7/.jigocoin -rpcwallet=miner07 listreceivedbyaddress 0 true"
    }

]

wallet_data = {}

# ---------------------------------------
# CONSULTAR NODOS
# ---------------------------------------

for node in nodes:

    print(f"🔎 Consultando {node['name']}...")

    try:

        result = subprocess.run(
            node["cmd"],
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        wallet_data[node["name"]] = result.stdout

    except Exception as e:

        print(f"⚠️ Error en {node['name']}: {e}")

# ---------------------------------------
# BUSCAR DIRECCIONES
# ---------------------------------------

print("\n=== RESULTADOS ===\n")

missing = []
total_found = 0

for addr, amount in sorted(
        address_totals.items(),
        key=lambda x: x[1],
        reverse=True):

    found = None

    for node_name, output in wallet_data.items():

        if addr in output:

            found = node_name
            break

    if found:

        total_found += amount

        print(
            f"{addr}  "
            f"{amount:12.2f} JGC  "
            f"→ {found}"
        )

    else:

        missing.append((addr, amount))

        print(
            f"{addr}  "
            f"{amount:12.2f} JGC  "
            f"⚠️ NO ENCONTRADA"
        )

print("\n--------------------------------")

missing_total = sum(a for _, a in missing)

print(f"TOTAL ENCONTRADO : {total_found:.2f} JGC")
print(f"TOTAL FALTANTE   : {missing_total:.2f} JGC")

print("\nDirecciones sin wallet:")

for addr, amount in missing:

    print(f"{addr}  {amount:.2f} JGC")

print("\n=== FIN ===\n")
