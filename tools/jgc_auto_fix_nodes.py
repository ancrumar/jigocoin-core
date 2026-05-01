#!/usr/bin/env python3

import subprocess
import json

ORCH_FILE = "/home/ancrumar/jigocoin/tools/jgc_transfer_orchestrator_v22_7.py"

# ---------------- RPC ----------------

def rpc(node, wallet, cmd, docker=False):

    if docker:
        base = [
            "docker", "exec", f"jigocoin-{node}",
            "/opt/jigocoin/build/bin/bitcoin-cli",
            "-datadir=/data",
            f"-rpcwallet={wallet}"
        ]
    else:
        base = [
            "/home/ancrumar/jigocoin/build/bin/bitcoin-cli",
            f"-rpcwallet={wallet}"
        ]

    out = subprocess.check_output(base + cmd, text=True)
    return out.strip()

# ---------------- CHECK ----------------

def is_valid(node, wallet, address, docker):

    try:
        data = rpc(node, wallet, ["getaddressinfo", address], docker)
        j = json.loads(data)
        return j.get("ismine", False)
    except:
        return False

# ---------------- FIX ----------------

def get_new_address(node, wallet, docker):

    addr = rpc(node, wallet, ["getnewaddress"], docker)
    return addr

# ---------------- MAIN ----------------

def main():

    print("=== AUTO FIX NODE CONSISTENCY ===")

    nodes = {
        "node1": ("miner01", False, "jgc1qhunsrpechm7uudqn0c352yqaj0v78we2n7acw0"),
        "node2": ("wallet2", True,  "jgc1qt68zd8pxqlyu7h9n95qm6qzgwfwf7xak49er03"),
        "node3": ("wallet3", True,  "jgc1qvu6gekmsmrr8t6sea2v58q25czrthrne5mxpdk"),
        "node4": ("wallet4", True,  "jgc1qcs7jddqqu5hcgz2f4rvnm78azfdeplrmmv6mn0"),
        "node5": ("wallet5", True,  "jgc1qj55xqhh8g9ume3422lp4vhwgsh0mkxkdcgn9k9"),
        "node7": ("miner07", False, "jgc1qfxkxlag9ecpa84zt54fs")
    }

    fixed = {}

    for node, (wallet, docker, addr) in nodes.items():

        print(f"\n🔎 {node}")

        ok = is_valid(node, wallet, addr, docker)

        if ok:
            print("✔ OK (ismine=true)")
            fixed[node] = addr
        else:
            print("❌ INVALID → regenerating...")

            new_addr = get_new_address(node, wallet, docker)
            print(f"✔ NEW ADDRESS: {new_addr}")

            fixed[node] = new_addr

    print("\n=== FIX SUMMARY ===")

    for k,v in fixed.items():
        print(k, "→", v)

    print("\n⚠️ NOTA: ahora debes actualizar el orchestrator manualmente o con script")

if __name__ == "__main__":
    main()
