#!/usr/bin/env python3

import subprocess
import json

print("=== AUTO FIX NODE CONSISTENCY v2 ===")

# ---------------- RPC CONFIG ----------------

nodes = {

    "node1": {
        "wallet": "miner01",
        "cmd": [
            "/home/ancrumar/jigocoin/build/bin/bitcoin-cli",
            "-rpcconnect=::1",
            "-rpcport=19336"
        ],
        "address": "jgc1qhunsrpechm7uudqn0c352yqaj0v78we2n7acw0"
    },

    "node2": {
        "wallet": "wallet2",
        "cmd": [
            "docker","exec","jigocoin-node2",
            "/opt/jigocoin/build/bin/bitcoin-cli",
            "-datadir=/data"
        ],
        "address": "jgc1qt68zd8pxqlyu7h9n95qm6qzgwfwf7xak49er03"
    },

    "node3": {
        "wallet": "wallet3",
        "cmd": [
            "docker","exec","jigocoin-node3",
            "/opt/jigocoin/build/bin/bitcoin-cli",
            "-datadir=/data"
        ],
        "address": "jgc1qvu6gekmsmrr8t6sea2v58q25czrthrne5mxpdk"
    }

}

# ---------------- RPC CALL ----------------

def rpc(node, args):

    base = nodes[node]["cmd"]
    wallet = nodes[node]["wallet"]

    cmd = base + [f"-rpcwallet={wallet}"] + args

    try:
        out = subprocess.check_output(cmd, text=True)
        return out.strip()

    except subprocess.CalledProcessError:
        return None

# ---------------- CHECK ----------------

def check_node(node):

    addr = nodes[node]["address"]

    print(f"\n🔎 {node}")

    info = rpc(node, ["getaddressinfo", addr])

    if not info:
        print("❌ RPC ERROR")
        return None

    data = json.loads(info)

    if data.get("ismine", False):
        print("✔ OK — address pertenece a wallet")
        return addr

    print("❌ Address no pertenece — regenerando...")

    new_addr = rpc(node, ["getnewaddress"])

    if new_addr:
        print(f"✔ NUEVA ADDRESS: {new_addr}")
        return new_addr

    print("❌ No se pudo generar address")
    return None

# ---------------- MAIN ----------------

fixed = {}

for node in nodes:

    new = check_node(node)

    if new:
        fixed[node] = new

print("\n=== RESULTADO FINAL ===")

for k,v in fixed.items():
    print(k,"→",v)

print("\n⚠️ Actualiza ahora el orchestrator con estas direcciones.")
