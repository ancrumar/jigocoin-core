#!/bin/bash

echo "=== AUDITORIA ORCHESTRATOR ADDRESSES ==="

declare -A nodes

nodes[node1]="miner01 jgc1qhunsrpechm7uudqn0c352yqaj0v78we2n7acw0"
nodes[node2]="wallet2 jgc1qt68zd8pxqlyu7h9n95qm6qzgwfwf7xak49er03"
nodes[node3]="wallet3 jgc1qvu6gekmsmrr8t6sea2v58q25czrthrne5mxpdk"
nodes[node4]="wallet4 jgc1qcs7jddqqu5hcgz2f4rvnm78azfdeplrmmv6mn0"
nodes[node5]="wallet5 jgc1qj55xqhh8g9ume3422lp4vhwgsh0mkxkdcgn9k9"
nodes[node7]="miner07 jgc1qfxkxlag9ecpa84zt54fs"

for node in "${!nodes[@]}"; do

    wallet=$(echo ${nodes[$node]} | cut -d' ' -f1)
    addr=$(echo ${nodes[$node]} | cut -d' ' -f2)

    echo ""
    echo "🔎 Node: $node"
    echo "   Wallet: $wallet"
    echo "   Address: $addr"

    if [[ "$node" == "node2" || "$node" == "node3" ]]; then

        info=$(docker exec jigocoin-$node \
        /opt/jigocoin/build/bin/bitcoin-cli \
        -datadir=/data \
        -rpcwallet=$wallet \
        getaddressinfo $addr 2>/dev/null)

    else

        info=$(~/jigocoin/build/bin/bitcoin-cli \
        -rpcwallet=$wallet \
        getaddressinfo $addr 2>/dev/null)

    fi

    if [ -z "$info" ]; then
        echo "❌ NO ENCONTRADA EN WALLET"
        continue
    fi

    if echo "$info" | grep -q '"ismine": true'; then
        echo "✔ PERTENECE A WALLET"
    else
        echo "⚠️ EXISTE PERO NO ES PROPIA"
    fi

done

echo ""
echo "=== FIN AUDITORIA ==="

