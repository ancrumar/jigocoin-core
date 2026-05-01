#!/bin/bash
export LC_ALL=C

echo
echo "=== ESTADO ECONOMICO JIGOCOIN ==="
echo

# --- TOTAL BLOCKCHAIN (desde node7 en hpblanco) ---

TOTAL=$(ssh hpblanco \
"/home/ancrumar/jigocoin/bin/bitcoin-cli \
-datadir=/home/ancrumar/jigocoin/node7/.jigocoin \
gettxoutsetinfo" \
| jq -r '.total_amount')

TOTAL=$(echo "$TOTAL" | tr ',' '.')

echo "Total blockchain : $TOTAL JGC"
echo

SUM=0

get_balance() {

NODE=$1
CMD=$2

START=$(date +%s.%N)

BAL=$(ssh hpblanco "$CMD" 2>/dev/null)

END=$(date +%s.%N)

BAL=$(echo "$BAL" | head -n1 | tr ',' '.')

# validar número
if [[ ! "$BAL" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    BAL=0
fi

TIME=$(echo "$END - $START" | bc)

printf "%-6s : %12.2f JGC (%.2fs)\n" "$NODE" "$BAL" "$TIME"

SUM=$(echo "$SUM + $BAL" | bc)

}

echo "Wallet balances:"
echo

get_balance node1 \
"docker exec jigocoin-node1 /opt/jigocoin/build/bin/bitcoin-cli -datadir=/data -rpcwallet=wallet1 getbalance"

get_balance node2 \
"docker exec jigocoin-node2 /opt/jigocoin/build/bin/bitcoin-cli -datadir=/data -rpcwallet=wallet2 getbalance"

get_balance node3 \
"docker exec jigocoin-node3 /opt/jigocoin/build/bin/bitcoin-cli -datadir=/data -rpcwallet=wallet3 getbalance"

get_balance node4 \
"docker exec jigocoin-node4 /opt/jigocoin/build/bin/bitcoin-cli -datadir=/data -rpcwallet=wallet4 getbalance"

get_balance node5 \
"docker exec jigocoin-node5 /opt/jigocoin/build/bin/bitcoin-cli -datadir=/data -rpcwallet=wallet5 getbalance"

get_balance node7 \
"/home/ancrumar/jigocoin/bin/bitcoin-cli \
-datadir=/home/ancrumar/jigocoin/node7/.jigocoin \
-rpcwallet=miner07 \
getbalance"

echo
echo "--------------------------------"

printf "Total wallets : %.2f JGC\n" "$SUM"

REST=$(echo "$TOTAL - $SUM" | bc)

printf "Fuera wallets : %.2f JGC\n" "$REST"

PERCENT=$(echo "scale=2; ($SUM/$TOTAL)*100" | bc)

printf "Controlado    : %.2f %%\n" "$PERCENT"

echo
