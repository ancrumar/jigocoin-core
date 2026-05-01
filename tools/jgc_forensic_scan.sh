#!/bin/bash

echo "======================================="
echo "   JIGOCOIN FORENSIC WALLET SCAN"
echo "======================================="

TARGET="jgc1qetnamuarr04hstay37pmyj9qxfylx3x9nj9l6v"

echo ""
echo "[1] BUSCANDO WALLETS (wallet.dat / backups)..."
find ~ /mnt /DATA /var/lib/docker -type f \( \
-name "wallet.dat" -o \
-name "*.dat" -o \
-name "*.bak" -o \
-name "*.old" -o \
-name "*.zip" -o \
-name "*.tar" \
\) 2>/dev/null | tee /tmp/jgc_wallets_found.txt

echo ""
echo "[2] BUSCANDO REFERENCIAS A DIRECCIÓN PERDIDA..."
grep -R "$TARGET" ~ 2>/dev/null | tee /tmp/jgc_address_refs.txt

echo ""
echo "[3] BUSCANDO SCRIPTS DE MINADO..."
grep -R "generatetoaddress" ~ 2>/dev/null | tee /tmp/jgc_mining_refs.txt

echo ""
echo "[4] BUSCANDO WALLET COMMANDS (dump / privkeys)..."
grep -R "dumpwallet\|importwallet\|getaddressinfo\|getnewaddress" ~ 2>/dev/null | tee /tmp/jgc_wallet_cmds.txt

echo ""
echo "[5] BUSCANDO EN DOCKER VOLUMES..."
find /var/lib/docker -type f 2>/dev/null | grep -i wallet | tee /tmp/jgc_docker_wallets.txt

echo ""
echo "======================================="
echo "SCAN COMPLETADO"
echo "RESULTADOS EN /tmp/"
echo "======================================="
