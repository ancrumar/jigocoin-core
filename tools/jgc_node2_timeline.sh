#!/bin/bash

TARGET="jgc1qetnamuarr04hstay37pmyj9qxfylx3x9nj9l6v"

echo "========================================"
echo "   JIGOCOIN NODE2 FORENSIC TIMELINE"
echo "========================================"

echo ""
echo "[1] BUSCANDO PRIMERA APARICION DE DIRECCION EN BLOCKCHAIN (CSV)..."
grep "$TARGET" ~/jigocoin_blocks.csv | head -n 20

echo ""
echo "[2] ORDENANDO BLOQUES DONDE APARECE..."

awk -F';' -v addr="$TARGET" '
$7==addr {print $1, $5, $11}
' ~/jigocoin_blocks.csv | sort -n | head -n 10

echo ""
echo "[3] CONSULTANDO BLOQUES EN NODE2 (DOCKER)..."

for h in $(docker exec jigocoin-node2 /opt/jigocoin/build/bin/bitcoin-cli -datadir=/data getblockcount); do
  echo "Block height: $h"
  break
done

echo ""
echo "[4] BUSCANDO EN LOGS DE NODE2..."

docker logs jigocoin-node2 2>&1 | grep -i "generatetoaddress\|$TARGET" | tail -n 50

echo ""
echo "[5] BUSCANDO ACTIVIDAD DE WALLET EN MOMENTO CRITICO..."

grep -R "wallet2\|miner01\|generate\|$TARGET" ~/mine-node2.sh 2>/dev/null

echo ""
echo "========================================"
echo " TIMELINE COMPLETO"
echo "========================================"
